"""Deterministic scheduler simulator for FIFO and length-aware micro-batching."""
from __future__ import annotations
from dataclasses import dataclass
import math, random

@dataclass(frozen=True)
class Request:
    request_id: int
    arrival_ms: float
    token_count: int

@dataclass
class RequestResult:
    request_id: int
    arrival_ms: float
    token_count: int
    start_ms: float
    finish_ms: float
    queue_ms: float
    latency_ms: float
    batch_size: int

@dataclass
class PolicySummary:
    policy: str
    request_count: int
    makespan_ms: float
    throughput_rps: float
    mean_queue_ms: float
    p95_queue_ms: float
    mean_latency_ms: float
    batches: int

def percentile(values, p):
    if not values: return 0.0
    values = sorted(values)
    return values[max(0, min(len(values)-1, math.ceil(p/100*len(values))-1))]

def generate_workload(count=100, seed=7, arrival_gap_ms=3.0, max_tokens=256):
    if count < 1 or arrival_gap_ms <= 0 or max_tokens < 1:
        raise ValueError("count, arrival_gap_ms, and max_tokens must be positive")
    rng = random.Random(seed)
    t = 0.0
    out = []
    for i in range(count):
        t += rng.expovariate(1.0 / arrival_gap_ms)
        tokens = min(max_tokens, max(8, int(rng.lognormvariate(3.7, 0.65))))
        out.append(Request(i, round(t, 3), tokens))
    return out

def summarize(policy, results, batch_count):
    if not results:
        return PolicySummary(policy, 0, 0, 0, 0, 0, 0, 0)
    first = min(r.arrival_ms for r in results)
    last = max(r.finish_ms for r in results)
    span = max(0.001, last-first)
    queues = [r.queue_ms for r in results]
    return PolicySummary(
        policy=policy, request_count=len(results), makespan_ms=round(last, 3),
        throughput_rps=round(len(results)/(span/1000), 3),
        mean_queue_ms=round(sum(queues)/len(queues), 3),
        p95_queue_ms=round(percentile(queues, 95), 3),
        mean_latency_ms=round(sum(r.latency_ms for r in results)/len(results), 3),
        batches=batch_count)

def run_fifo(requests, base_ms=2.0, per_token_ms=0.08):
    now, results = 0.0, []
    for req in sorted(requests, key=lambda r: (r.arrival_ms, r.request_id)):
        start = max(now, req.arrival_ms)
        finish = start + base_ms + per_token_ms * req.token_count
        results.append(RequestResult(req.request_id, req.arrival_ms, req.token_count,
            round(start,3), round(finish,3), round(start-req.arrival_ms,3),
            round(finish-req.arrival_ms,3), 1))
        now = finish
    return results, len(results)

def run_batched(requests, max_batch_size=8, max_wait_ms=4.0,
                base_ms=2.0, per_token_ms=0.08, efficiency_floor=0.62):
    if max_batch_size < 1 or max_wait_ms < 0 or not (0 < efficiency_floor <= 1):
        raise ValueError("invalid batch configuration")
    ordered = sorted(requests, key=lambda r: (r.arrival_ms, r.request_id))
    pending, idx, now, results, batches = [], 0, 0.0, [], 0
    while idx < len(ordered) or pending:
        if not pending and idx < len(ordered):
            now = max(now, ordered[idx].arrival_ms)
            pending.append(ordered[idx]); idx += 1
        deadline = pending[0].arrival_ms + max_wait_ms
        while idx < len(ordered) and len(pending) < max_batch_size:
            next_req = ordered[idx]
            if next_req.arrival_ms > deadline:
                break
            pending.append(next_req); idx += 1
        start = max(now, pending[0].arrival_ms)
        total_tokens = sum(r.token_count for r in pending)
        factor = max(efficiency_floor, 1.0 / math.sqrt(len(pending)))
        service = base_ms + per_token_ms * total_tokens * factor
        finish = start + service
        for req in pending:
            results.append(RequestResult(req.request_id, req.arrival_ms, req.token_count,
                round(start,3), round(finish,3), round(start-req.arrival_ms,3),
                round(finish-req.arrival_ms,3), len(pending)))
        now, pending, batches = finish, [], batches+1
    results.sort(key=lambda r: r.request_id)
    return results, batches
