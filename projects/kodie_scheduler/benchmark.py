#!/usr/bin/env python3
import argparse, csv, json
from dataclasses import asdict
from pathlib import Path
from scheduler import generate_workload, run_fifo, run_batched, summarize

def main():
    p = argparse.ArgumentParser(description="Compare FIFO and batched scheduler simulations.")
    p.add_argument("--requests", type=int, default=500)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--arrival-gap-ms", type=float, default=3.0)
    p.add_argument("--max-batch-size", type=int, default=8)
    p.add_argument("--max-wait-ms", type=float, default=4.0)
    p.add_argument("--out", default="results/kodie")
    a = p.parse_args()
    workload = generate_workload(a.requests, a.seed, a.arrival_gap_ms)
    fifo, fb = run_fifo(workload)
    batched, bb = run_batched(workload, a.max_batch_size, a.max_wait_ms)
    summaries = [asdict(summarize("fifo", fifo, fb)), asdict(summarize("batched", batched, bb))]
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    (out/"summary.json").write_text(json.dumps({
        "experiment_type": "simulation_not_gpu_benchmark",
        "config": vars(a), "summaries": summaries
    }, indent=2)+"\n", encoding="utf-8")
    with (out/"requests.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["policy","request_id","arrival_ms","token_count","start_ms","finish_ms","queue_ms","latency_ms","batch_size"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for policy, rows in [("fifo", fifo), ("batched", batched)]:
            for row in rows:
                w.writerow({"policy":policy, **asdict(row)})
    print(json.dumps(summaries, indent=2))
if __name__ == "__main__":
    main()
