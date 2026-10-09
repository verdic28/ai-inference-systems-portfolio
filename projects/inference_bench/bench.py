#!/usr/bin/env python3
"""Measure synthetic or OpenAI-compatible HTTP inference request latency."""
from __future__ import annotations
import argparse, concurrent.futures, json, os, platform, random, time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

def percentile(values, p):
    if not values:
        return None
    xs = sorted(values)
    index = max(0, min(len(xs)-1, int((p / 100) * len(xs) + 0.999999) - 1))
    return round(xs[index] * 1000, 3)

def synthetic_request(seed):
    # Deterministic small CPU workload to exercise the harness, not an LLM.
    rng = random.Random(seed)
    start = time.perf_counter()
    _ = sum((rng.random() ** 2) for _ in range(250))
    return time.perf_counter() - start

def http_request(url, model, api_key, prompt, max_tokens, timeout):
    payload = json.dumps({
        "model": model, "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens, "temperature": 0
    }).encode()
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    req = Request(url, data=payload, headers=headers, method="POST")
    start = time.perf_counter()
    with urlopen(req, timeout=timeout) as response:
        body = response.read()
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(f"HTTP status {response.status}")
        json.loads(body.decode("utf-8"))
    return time.perf_counter() - start

def run(args):
    if args.requests < 1 or args.concurrency < 1 or args.warmup < 0:
        raise ValueError("requests/concurrency must be positive; warmup cannot be negative")
    mode = args.mode
    url = os.getenv("INFERENCE_BENCH_URL")
    model = os.getenv("INFERENCE_BENCH_MODEL", "model-not-set")
    api_key = os.getenv("INFERENCE_BENCH_API_KEY")
    if mode == "http" and not url:
        raise ValueError("Set INFERENCE_BENCH_URL to an OpenAI-compatible chat-completions endpoint")
    def one(i):
        if mode == "synthetic":
            return synthetic_request(args.seed + i)
        return http_request(url, model, api_key, args.prompt, args.max_tokens, args.timeout)
    for i in range(args.warmup):
        one(-args.warmup + i)
    latencies, errors = [], []
    wall_start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = {pool.submit(one, i): i for i in range(args.requests)}
        for future in concurrent.futures.as_completed(futures):
            try:
                latencies.append(future.result())
            except Exception as exc:
                errors.append({"request": futures[future], "error": f"{type(exc).__name__}: {exc}"})
    duration = time.perf_counter() - wall_start
    summary = {
        "mode": mode, "requests_requested": args.requests,
        "successful_requests": len(latencies), "failed_requests": len(errors),
        "concurrency": args.concurrency, "warmup_requests": args.warmup,
        "duration_seconds": round(duration, 6),
        "throughput_requests_per_second": round(len(latencies) / duration, 3) if duration else None,
        "latency_ms_p50": percentile(latencies, 50),
        "latency_ms_p95": percentile(latencies, 95),
        "model": model if mode == "http" else None,
        "endpoint": url if mode == "http" else None,
        "python": platform.python_version(), "platform": platform.platform(),
        "notes": "Synthetic mode is not model inference." if mode == "synthetic" else
                 "Client-observed latency includes network and server effects.",
        "errors": errors[:10]
    }
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["synthetic", "http"], default="synthetic")
    parser.add_argument("--requests", type=int, default=100)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--warmup", type=int, default=2)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--prompt", default="Reply with the word READY.")
    parser.add_argument("--max-tokens", type=int, default=16)
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("--out", help="Optional path for JSON summary")
    args = parser.parse_args()
    try:
        result = run(args)
        print(json.dumps(result, indent=2))
        if result["failed_requests"]:
            raise SystemExit(2)
    except (ValueError, URLError, HTTPError) as exc:
        parser.error(str(exc))
if __name__ == "__main__":
    main()
