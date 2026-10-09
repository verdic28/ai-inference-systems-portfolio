# Portfolio guide: how to run, inspect, and present the projects

## Recommended order
1. Run tests and inspect the CI workflow.
2. Run the synthetic inference benchmark to learn the output format.
3. Run the scheduler benchmark with multiple seeds and workload sizes.
4. If you have access to a model server, run the HTTP benchmark and preserve the exact configuration.
5. Pick a real upstream issue only after reproducing it locally; do not describe the contribution kit itself as an upstream contribution.

## Suggested demo script
```bash
python -m unittest discover -s tests -v
python projects/inference_bench/bench.py --mode synthetic --requests 500 --concurrency 8 --seed 11
python projects/kodie_scheduler/benchmark.py --requests 1000 --seed 7 --out results/kodie
python projects/oss_contribution_kit/check_repo.py .
```

## How to describe this honestly on a resume
- Built a Python inference benchmark CLI reporting latency percentiles, throughput, failures, and environment metadata for synthetic or OpenAI-compatible HTTP endpoints.
- Implemented a deterministic scheduler simulator comparing FIFO execution with length-aware micro-batching; exported per-policy metrics and request-level results.
- Added unit tests and GitHub Actions CI; created a repository hygiene checker and structured upstream contribution workflow.

Only add numerical outcomes after running the tools in the environment you intend to report. Do not present simulator output as measured GPU performance.

## Before applying
- Replace any placeholder links with the actual public repository and demo.
- Run the full test suite locally and in GitHub Actions.
- For HTTP benchmark reports, record GPU/CPU model, model ID, quantization, server version, prompt/output lengths, concurrency, warm-up count, and date.
- If results vary, run at least 3 repetitions and report median plus spread rather than selecting the best run.
