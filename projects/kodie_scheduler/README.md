# KODIE Scheduler Lab

A deterministic discrete-work simulator comparing FIFO request execution with a simple length-aware micro-batching policy.

## Run
```bash
python projects/kodie_scheduler/benchmark.py --requests 500 --seed 7 --out results/kodie
```

The tool writes `summary.json` and request-level `requests.csv`. Change `--arrival-gap-ms`, `--max-batch-size`, and `--max-wait-ms` to explore the trade-off between waiting to form batches and completing requests.

## Metrics
Per-policy output includes request count, makespan, simulated throughput, mean/p95 queue time, mean latency, and batch count.

## Limitations
This is a simulator, not a GPU benchmark. Its service-time model does not reproduce CUDA execution, GPU memory behavior, KV-cache pressure, or production vLLM scheduling. Do not present these numbers as measured tokens/second or hardware speedups.
