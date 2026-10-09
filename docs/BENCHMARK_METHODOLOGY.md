# Benchmark methodology and reporting rules

## Inference Bench Lab
- Synthetic mode uses a local deterministic function and exists to validate the measurement pipeline. It does not run a language model.
- HTTP mode sends requests to an OpenAI-compatible chat-completions endpoint.
- Warm-up requests are excluded from the measured sample.
- Reported latency is client-observed wall time, so it includes network and server queueing.
- Throughput is successful requests divided by measured wall-clock duration.
- p50 and p95 are nearest-rank percentiles of successful request latencies.
- Errors are counted separately; a run with errors must not be reported as a clean performance result.

For meaningful model-serving comparisons, keep model, prompt set, output token cap, hardware, server version, quantization, and concurrency fixed.

## KODIE Scheduler Lab
This is a discrete-work simulation. Each request has a deterministic arrival time and estimated service cost. FIFO processes one request at a time. The batching policy groups requests up to a maximum batch size and applies a configurable batch service-time model.

Simulator outputs can compare algorithm behavior under the same generated workload, but they do not model CUDA kernels, GPU memory, real KV cache behavior, or all vLLM scheduler details. Do not claim simulated throughput as real tokens/second.

## Reproducibility checklist
- Save exact CLI arguments and seed.
- Preserve raw CSV and summary JSON.
- Run repeated trials with different seeds.
- State whether results are simulated, synthetic, or collected from a real endpoint.
- Report hardware/software versions and any failures.


## Published repeated-seed scheduler run

The checked-in artifact [`results/scheduler_simulation_500_10_seeds.json`](../results/scheduler_simulation_500_10_seeds.json) records 10 seeded simulations of 500 requests each (seeds 0–9), with an 8-request batch cap and 4 ms collection window.

Across those seeds, the simulator's arithmetic mean was:

| Metric | FIFO | Micro-batching | Change |
|---|---:|---:|---:|
| Simulated requests/s | 168.501 | 280.127 | +66.2% |
| Mean completion time / makespan (ms) | 2971.277 | 1788.721 | -39.8% |
| Mean modeled latency (ms) | 744.554 | 157.866 | -78.8% |
| Mean queue time (ms) | 738.617 | 148.422 | -79.9% |
| p95 queue time (ms) | 1397.134 | 279.280 | -80.0% |
| Mean number of batches | 500.0 | 212.7 | -57.5% |

These results describe only the simulator's workload and service-time assumptions. They are not measurements of a real GPU, model server, tokens/s, or production latency. The inference benchmark's synthetic mode is a harness smoke test, not model inference.
