# Inference Bench Lab

A small CLI for measuring client-observed latency and throughput of an OpenAI-compatible `/v1/chat/completions` endpoint. A synthetic mode validates the harness without requiring a model or GPU.

## Install
Core/synthetic mode: Python 3.10+, no third-party dependencies.

HTTP mode uses `requests`:
```bash
python -m pip install -r projects/inference_bench/requirements-optional.txt
```

## Synthetic smoke test
```bash
python projects/inference_bench/bench.py --mode synthetic --requests 200 --concurrency 8 --seed 5
```

## Real endpoint
Start an OpenAI-compatible server (for example, vLLM) and set:
```bash
export INFERENCE_BENCH_URL=http://localhost:8000/v1/chat/completions
export INFERENCE_BENCH_MODEL=your-model-name
export INFERENCE_BENCH_API_KEY=your-key-if-needed
python projects/inference_bench/bench.py --mode http --requests 30 --concurrency 4 --warmup 3
```
Environment variables are preferred to avoid putting keys in shell history. Never commit API keys.

## Output
The command prints a JSON summary including mode, request count, successful/failed requests, p50/p95 latency, throughput, concurrency, and runtime metadata. Use `--out results/run.json` to save it.

## Interpretation
HTTP latency includes client/network/server effects. Synthetic results are harness checks, not model performance. Compare only runs with the same model, server, hardware, prompt, output cap, and workload.
