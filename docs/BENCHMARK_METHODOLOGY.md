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
