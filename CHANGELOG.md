# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2025-12-22

### Added
- **Reproducibility Contract**: Explicit contract defining what is captured, what is best-effort, and what is NOT guaranteed
- **Enhanced Validation Command**: Comprehensive validation with JSON output, checks for environment capture, seed info, and reproducibility contract
- **CLI `info` command**: Display reproducibility contract and phytrace information
- Reproducibility contract included in all evidence pack manifests

### Changed
- **Invariant Semantics Clarification**: Documentation now explicitly states invariants are runtime diagnostics, not formal proofs
- **Documentation Tightening**: Added positioning statement, "Why not DVC/MLflow/git?" section, and improved clarity
- Enhanced `validate` command with comprehensive checks and warnings
- README updated with reproducibility contract information

### Fixed
- Validation command now checks for reproducibility contract presence
- Improved error messages and validation reporting

## [0.1.1] - 2025-12-22

### Changed
- TestPyPI republish after deletion; no functional changes

## [0.1.0] - 2025-12-20

### Added
- Core `trace_run` function wrapping scipy.integrate.solve_ivp
- Environment capture (Python version, packages, git state, system info)
- Seed management for deterministic execution
- Invariant checking system with built-in invariants (finite, bounded, monotonic)
- Custom invariant decorator (`@create_invariant`)
- Evidence pack generation with structured directory layout (stable schema)
- Automatic plot generation (time series, phase space, solver stats)
- Manifest generation with complete metadata
- Golden test framework for regression testing (basic functionality)
- Comprehensive test suite (28 tests, all passing)
- Example simulations (damped oscillator, double pendulum)
- Documentation (README, type hints, docstrings)

### Future Work (v0.2.0)
- CLI tools for validation and comparison
- Configuration system via TOML and environment variables
- Jupyter notebook integration
- Multi-solver comparison
- Assumption ledger
- Sphinx documentation website

### Features
- Zero refactoring required - drop-in replacement for solve_ivp
- Automatic provenance tracking
- Runtime invariant verification
- Structured evidence packs
- Deterministic by default

### Known Limitations
- No formal verification capabilities
- No real-time guarantees
- No certification claims
- Performance overhead not yet fully optimized (target < 5%)
- Some optional features require additional dependencies

### Breaking Changes
None (initial release)

