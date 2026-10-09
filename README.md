# AI Inference Systems Portfolio

Engineering portfolio focused on inference benchmarking, scheduling experiments, and reproducible systems tooling.

## Projects

- **Inference benchmark suite** — a request-latency/throughput harness with a clearly labelled synthetic mode. Synthetic results are not real LLM or GPU performance claims.
- **KODIE scheduler simulation** — a small scheduling simulator and benchmark for exploring workload policies. Simulation results are not hardware speedups.
- **Open-source contribution kit** — repository checks and a practical contribution checklist.

## Run tests

```bash
python -m pip install pytest
python -m pytest -q
```

See [`docs/PORTFOLIO_GUIDE.md`](docs/PORTFOLIO_GUIDE.md) and [`docs/BENCHMARK_METHODOLOGY.md`](docs/BENCHMARK_METHODOLOGY.md) for scope, setup, and benchmark interpretation.

## Important limitations

The included benchmarks are synthetic or simulated unless explicitly stated otherwise. No real GPU acceleration, production inference performance, or upstream open-source contribution is claimed by this repository.
