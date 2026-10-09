# Open-source Contribution Engineering Kit

A practical toolkit for making a contribution reproducible, reviewable, and safe. It includes a lightweight repository hygiene checker and templates/checklists.

**Important:** using this kit does not itself constitute an upstream contribution. Only list an upstream contribution on your resume after opening the real PR and linking it accurately.

## Run checker
```bash
python projects/oss_contribution_kit/check_repo.py .
```

The checker reports missing common project files and accidental-looking secret patterns. It is a heuristic and may produce false positives/negatives. Do not use it as a security scanner.

## Contribution workflow
1. Read `CONTRIBUTING_CHECKLIST.md`.
2. Find an issue in an upstream repository and check that it is still open and in scope.
3. Reproduce the bug with the smallest test case possible.
4. Write a failing test first when practical.
5. Make a focused change; avoid unrelated formatting churn.
6. Run the project test/lint/type-check commands.
7. Document behavior change and compatibility impact.
8. Open a PR with before/after evidence and link the issue.
9. Respond constructively to review and update the PR.
