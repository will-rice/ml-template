# Task 1 Report

## Summary

Updated the ML template dependency floors to current releases, regenerated `uv.lock`, and verified the canonical CI workflow and pre-commit setup without needing source or test changes.

## Files Changed

- `pyproject.toml`
- `uv.lock`

## Commands and Results

- `git rev-parse HEAD && git status --short` — recorded baseline commit and status.
- `uv lock --check && uv run pre-commit run -a && git status --short` — baseline checks passed cleanly.
- `uv remove ... && uv add ... && UV_BUILD_VERSION=... && uv lock --upgrade` — refreshed dependency floors and regenerated the lockfile.
- `uv run pre-commit autoupdate` — remote hooks were already at the latest released revisions.
- `test "$(find .github/workflows -maxdepth 1 -type f | wc -l | tr -d ' ')" -eq 1 && test -f .github/workflows/ci.yml && grep -q '^name: ci$' .github/workflows/ci.yml` — canonical CI workflow verified.
- `uv lock --check && uv run pre-commit run -a && git diff --check` — final validation passed after formatting settled.

## Commit

- `ffe67898e4b27187fdd47af2a03551f44103a2c8`

## Pull Request

- `https://github.com/will-rice/ml-template/pull/14`

## Self-Review

- The dependency refresh is localized to the manifest and lockfile.
- Validation covers lockfile consistency, pre-commit hooks, diff cleanliness, and the canonical CI workflow.
- No source, test, or documentation edits were required because the upgrades did not break compatibility.

## Concerns

- None.
