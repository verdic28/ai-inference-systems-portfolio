import importlib.util, pathlib, tempfile, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_repo", ROOT/"projects/oss_contribution_kit/check_repo.py")
checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)

class RepoCheckerTests(unittest.TestCase):
    def test_reports_missing_readme(self):
        with tempfile.TemporaryDirectory() as d:
            result = checker.check_repo(d)
            self.assertTrue(any("README.md" in item for item in result))
    def test_detects_token_pattern(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d)
            (p/"README.md").write_text("project", encoding="utf-8")
            (p/"LICENSE").write_text("MIT", encoding="utf-8")
            (p/"sample.txt").write_text('token = "ghp_' + "A"*30 + '"', encoding="utf-8")
            result = checker.check_repo(p)
            self.assertTrue(any("possible secret pattern" in item for item in result))
    def test_clean_repo(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d)
            (p/"README.md").write_text("project", encoding="utf-8")
            (p/"LICENSE").write_text("MIT", encoding="utf-8")
            self.assertTrue(checker.check_repo(p)[0].startswith("OK:"))

if __name__ == "__main__": unittest.main()
