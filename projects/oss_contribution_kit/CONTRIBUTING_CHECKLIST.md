# Upstream contribution checklist

## Before coding
- [ ] Confirm the issue is current, in scope, and not already assigned/resolved.
- [ ] Read `CONTRIBUTING.md`, code of conduct, license, and local test instructions.
- [ ] Reproduce the issue on the upstream version and record exact environment/version.
- [ ] Identify expected behavior and write a minimal reproduction.

## Implementation
- [ ] Create a focused branch and make the smallest useful change.
- [ ] Add or update a regression test.
- [ ] Run focused tests, full relevant tests, formatter, linter, and type checker.
- [ ] Check backwards compatibility and error paths.
- [ ] Avoid secrets, generated artifacts, unrelated refactors, and undocumented dependencies.

## Pull request
- [ ] State problem, root cause, fix, and trade-offs.
- [ ] Include test commands and actual outputs.
- [ ] Include benchmark methodology if making performance claims.
- [ ] Link the issue and include screenshots only when useful.
- [ ] Never claim a PR is merged until upstream confirms it.
