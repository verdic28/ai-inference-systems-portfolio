import importlib.util, pathlib, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bench", ROOT/"projects/inference_bench/bench.py")
bench = importlib.util.module_from_spec(spec); spec.loader.exec_module(bench)

class InferenceBenchTests(unittest.TestCase):
    def test_percentile_empty(self):
        self.assertIsNone(bench.percentile([], 95))
    def test_percentile_nearest_rank(self):
        self.assertEqual(bench.percentile([0.001,0.002,0.003,0.004], 50), 2.0)
        self.assertEqual(bench.percentile([0.001,0.002,0.003,0.004], 95), 4.0)
    def test_synthetic_run_reports_successes(self):
        import argparse
        args = argparse.Namespace(mode="synthetic", requests=8, concurrency=2, warmup=1,
            seed=1, prompt="test", max_tokens=2, timeout=1, out=None)
        result = bench.run(args)
        self.assertEqual(result["successful_requests"], 8)
        self.assertEqual(result["failed_requests"], 0)
        self.assertIsNotNone(result["latency_ms_p95"])
    def test_invalid_requests(self):
        import argparse
        args = argparse.Namespace(mode="synthetic", requests=0, concurrency=1, warmup=0,
            seed=1, prompt="test", max_tokens=2, timeout=1, out=None)
        with self.assertRaises(ValueError): bench.run(args)

if __name__ == "__main__": unittest.main()
