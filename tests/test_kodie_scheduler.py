import importlib.util, pathlib, unittest, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("scheduler", ROOT/"projects/kodie_scheduler/scheduler.py")
sched = importlib.util.module_from_spec(spec); sys.modules[spec.name] = sched; spec.loader.exec_module(sched)

class SchedulerTests(unittest.TestCase):
    def test_workload_is_reproducible(self):
        self.assertEqual(sched.generate_workload(10, seed=3), sched.generate_workload(10, seed=3))
    def test_fifo_completes_every_request(self):
        reqs = sched.generate_workload(25, seed=1)
        results, batches = sched.run_fifo(reqs)
        self.assertEqual(len(results), len(reqs))
        self.assertEqual(batches, len(reqs))
        self.assertTrue(all(r.finish_ms >= r.start_ms for r in results))
    def test_batched_completes_each_request_once(self):
        reqs = sched.generate_workload(50, seed=9)
        results, batches = sched.run_batched(reqs, max_batch_size=5)
        self.assertEqual(sorted(r.request_id for r in results), list(range(50)))
        self.assertGreater(batches, 0)
        self.assertTrue(all(r.batch_size <= 5 for r in results))
    def test_invalid_batch_config(self):
        with self.assertRaises(ValueError):
            sched.run_batched(sched.generate_workload(2), max_batch_size=0)
    def test_summary_count(self):
        reqs = sched.generate_workload(10)
        results, n = sched.run_fifo(reqs)
        summary = sched.summarize("fifo", results, n)
        self.assertEqual(summary.request_count, 10)

if __name__ == "__main__": unittest.main()
