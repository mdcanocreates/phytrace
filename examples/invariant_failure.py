"""
Example: Invariant Failure

This example demonstrates what happens when invariants are violated,
and clarifies that invariants are runtime diagnostics, not formal proofs.

A violation indicates a potential issue but does not necessarily mean
the physics is incorrect. Similarly, passing invariants do not prove
correctness.
"""

import numpy as np
from phytrace import trace_run
from phytrace.invariants import bounded, finite, create_invariant


def exponential_growth(t, y, k):
    """
    Simple exponential growth: dy/dt = k*y
    
    If k > 0, this will grow unbounded, which may violate a bounded invariant.
    This is expected behavior for exponential growth, not an error.
    """
    return k * y


# Example 1: Warning-level invariant violation
# This will log violations but continue the simulation
print("=" * 60)
print("Example 1: Warning-level invariant violation")
print("=" * 60)

@create_invariant(name="bounded_warning", severity="warning")
def bounded_warning(t, y, params):
    """Warning-level bounded check."""
    return np.all((np.asarray(y) >= -5.0) & (np.asarray(y) <= 5.0))

bound_check_warning = bounded_warning

result1 = trace_run(
    simulate=exponential_growth,
    params={'k': 0.5},  # Positive growth rate
    t_span=(0, 5),
    y0=[1.0],
    invariants=[bound_check_warning],
    evidence_dir=None  # Don't create evidence for this quick example
)

print(f"Simulation completed: {result1.success}")
print(f"Checks passed: {result1.checks_passed}")
if result1.invariant_log:
    for inv in result1.invariant_log.get('invariants', []):
        print(f"  {inv['name']}: {inv['violations']}/{inv['checks']} violations")
print()


# Example 2: Error-level invariant violation
# This will log violations, set checks_passed=False, but continue
print("=" * 60)
print("Example 2: Error-level invariant violation")
print("=" * 60)

@create_invariant(name="bounded_error", severity="error")
def bounded_error(t, y, params):
    """Error-level bounded check."""
    return np.all((np.asarray(y) >= -2.0) & (np.asarray(y) <= 2.0))

bound_check_error = bounded_error

result2 = trace_run(
    simulate=exponential_growth,
    params={'k': 1.0},  # Faster growth
    t_span=(0, 3),
    y0=[1.0],
    invariants=[bound_check_error],
    evidence_dir=None
)

print(f"Simulation completed: {result2.success}")
print(f"Checks passed: {result2.checks_passed}")  # Will be False
if result2.invariant_log:
    for inv in result2.invariant_log.get('invariants', []):
        print(f"  {inv['name']}: {inv['violations']}/{inv['checks']} violations")
print()


# Example 3: Critical invariant violation
# This will stop the simulation immediately
print("=" * 60)
print("Example 3: Critical invariant violation (simulation stops)")
print("=" * 60)

@create_invariant(name="never_exceeds_10", severity="critical")
def never_exceeds_10(t, y, params):
    """Critical invariant: value must never exceed 10."""
    return np.all(np.asarray(y) <= 10.0)

try:
    result3 = trace_run(
        simulate=exponential_growth,
        params={'k': 2.0},  # Very fast growth
        t_span=(0, 5),
        y0=[1.0],
        invariants=[never_exceeds_10],
        evidence_dir=None
    )
    print("ERROR: Simulation should have stopped!")
except RuntimeError as e:
    print(f"✓ Simulation correctly stopped: {e}")
print()


# Example 4: False positive - invariant violation doesn't mean error
print("=" * 60)
print("Example 4: Invariant violation is not necessarily an error")
print("=" * 60)
print("""
The exponential growth function violates the bounded invariant,
but this is EXPECTED behavior for exponential growth, not an error.

Invariants are runtime diagnostics that help catch:
- Numerical errors (NaN, inf)
- Unexpected behavior
- Implementation bugs

But they do NOT prove:
- That the physics is correct
- That the implementation is correct
- That the results are valid

A violation means "check this" not "this is wrong".
""")

print("\n✓ Invariant failure examples complete!")
print("\nKey takeaway: Invariants are diagnostics, not proofs.")

