<!--
Thanks for contributing! Fill out what's relevant; delete sections that don't apply.
-->

## Summary

What does this PR change, and why? One or two sentences is fine.

## Type of change

- [ ] New defense pattern
- [ ] New attack variant or dataset addition
- [ ] Framework integration
- [ ] Notebook update
- [ ] Documentation / guide page
- [ ] Bug fix
- [ ] Refactor / repo hygiene
- [ ] Other (describe in summary)

## Test plan

How did you verify this works? Check what applies and add specifics.

- [ ] `uv run ruff check src/ tests/ benchmark/` passes
- [ ] `uv run ruff format --check src/ tests/ benchmark/` passes
- [ ] `uv run pytest tests/ -v --tb=short` passes
- [ ] `uv run python benchmark/run.py` runs end-to-end
- [ ] Affected notebook(s) open and run in `uv run marimo edit`
- [ ] `uv run mkdocs build --strict` passes (if docs changed)

For new defenses: tests cover (1) attacks are blocked, (2) legitimate inputs pass through, (3) edge cases (empty input, configuration variants).

For new attack variants: at least one existing defense's behavior against the variant is documented.

## Notes for reviewers

Anything tricky, intentional, or worth flagging during review (design tradeoffs, follow-up work, known limitations).

## Related issues

Closes #
Refs #
