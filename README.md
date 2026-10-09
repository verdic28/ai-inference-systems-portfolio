# AI Inference Systems Portfolio

A small engineering portfolio focused on inference measurement, scheduling experiments, and reproducible systems tooling.

## Projects

- **Inference Bench Lab** — Python CLI measuring client-observed latency, p50/p95, throughput, and failures for synthetic workloads or an OpenAI-compatible chat-completions endpoint.
- **KODIE Scheduler Lab** — deterministic simulation comparing FIFO scheduling with a simple micro-batching policy; exports summary JSON and per-request CSV.
- **Open-source Contribution Engineering Kit** — repository hygiene checker, issue template, and a checklist for making upstream contributions reproducible.

## Quick start

Requires Python 3.10+; the synthetic benchmark and scheduler simulation use the standard library.

```bash
python -m unittest discover -s tests -v
python projects/inference_bench/bench.py --mode synthetic --requests 100 --concurrency 4 --seed 7
python projects/kodie_scheduler/benchmark.py --requests 500 --seed 7 --out results/kodie
python projects/oss_contribution_kit/check_repo.py .
```

## Documentation

- [Portfolio guide](docs/PORTFOLIO_GUIDE.md)
- [Benchmark methodology and limitations](docs/BENCHMARK_METHODOLOGY.md)
- [Inference Bench Lab](projects/inference_bench/README.md)
- [KODIE Scheduler Lab](projects/kodie_scheduler/README.md)
- [Open-source contribution kit](projects/oss_contribution_kit/README.md)

## Honest interpretation of results

The synthetic inference mode does **not** run a language model. KODIE is a discrete-work simulation, not a GPU benchmark. Neither should be presented as measured GPU speedups or production tokens/second. Real endpoint results must include the model/server/hardware configuration and be reproducible. The contribution kit is not itself an upstream contribution; only claim upstream work after a real PR exists.

GitHub Actions runs the unit tests and smoke checks on pushes and pull requests.
