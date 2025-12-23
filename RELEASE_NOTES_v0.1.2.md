# Release v0.1.2: Credibility & Tightening

**Release Date**: 2025-12-22

## Summary

v0.1.2 focuses on making claims precise, testable, and defensible. This release answers skeptics and stabilizes semantics without introducing new features or expanding scope.

## What's New

### Reproducibility Contract

We now provide an explicit, inspectable contract that defines:
- **What is captured**: 14 items including Python version, packages, seeds, solver config, etc.
- **What is best-effort**: 5 items like git info, exact bit reproducibility
- **What is NOT guaranteed**: 8 items like cross-architecture determinism

The contract is:
- Included in all evidence pack manifests
- Accessible via `phytrace info` command
- Documented in README

### Enhanced Validation Command

The `phytrace validate` command now performs comprehensive checks:
- Manifest completeness
- Environment capture presence
- Seed information verification
- Reproducibility contract presence
- File structure integrity

New features:
- `--json` flag for machine-readable output
- Distinction between issues and warnings
- Detailed summary reporting

### CLI `info` Command

New command to display the reproducibility contract:
```bash
phytrace info
```

Shows what phytrace guarantees, what is best-effort, and what is explicitly not guaranteed.

### Invariant Semantics Clarification

Documentation now explicitly states:
- Invariants are **runtime diagnostics**, not formal proofs
- A violation does not necessarily mean the physics is incorrect
- A passing invariant does not prove correctness

Added example (`examples/invariant_failure.py`) demonstrating invariant violations.

### Documentation Tightening

- Added positioning statement: "Audit-ready tracing, not certification or formal verification"
- Added "Why not DVC / MLflow / git?" section with neutral comparisons
- Improved clarity throughout README
- 60-second readability improvements

## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete details.

## Installation

```bash
pip install phytrace
```

Or from TestPyPI (for testing):
```bash
pip install --index-url https://test.pypi.org/simple/ phytrace
```

## Migration Guide

No breaking changes. All existing code continues to work.

New evidence packs will automatically include the reproducibility contract in `manifest.json`.

## What's Next (v0.1.3)

Planned improvements based on community feedback:
- Reproducibility hardening (lockfile detection, SHA256 checksums)
- `phytrace export --zip` for shareable evidence packs
- `phytrace doctor` for environment diagnostics
- Optional SED-ML metadata stub

