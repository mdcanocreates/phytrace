"""
Damped Harmonic Oscillator Example

This is the canonical "hello world" example for phytrace, demonstrating
all core features: environment capture, invariant checking, and evidence generation.

The system: x'' + (c/m)x' + (k/m)x = 0
State: [x, v] where x is position and v is velocity
"""

import numpy as np
from phytrace import trace_run
from phytrace.invariants import bounded, finite, create_invariant


def damped_oscillator(t, y, k, c, m):
    """
    Right-hand side of the damped harmonic oscillator ODE.
    
    The equation is: x'' + (c/m)x' + (k/m)x = 0
    Converting to first-order: [x, v]' = [v, -(k/m)x - (c/m)v]
    
    Args:
        t: Time
        y: State vector [x, v]
        k: Spring constant
        c: Damping coefficient
        m: Mass
    
    Returns:
        Derivative [dx/dt, dv/dt]
    """
    x, v = y
    return [v, -(k/m)*x - (c/m)*v]


# Define invariants to check during simulation

# 1. Finite check: Ensure no NaN or inf values appear
#    This is critical - if violated, the simulation is invalid
finite_check = finite()

# 2. Bounded check: Position and velocity should stay within reasonable bounds
#    For a damped oscillator starting at x=1, v=0, we expect |x| < 2, |v| < 2
#    This is an error-level check - violations indicate potential issues
bound_check = bounded(-2.0, 2.0)

# 3. Energy check: Total energy should decrease (or stay constant for undamped)
#    Energy: E = 0.5*m*v^2 + 0.5*k*x^2
#    For damped system, energy should monotonically decrease
@create_invariant(name="energy_decreasing", severity="warning")
def energy_decreasing(t, y, params, **kwargs):
    """Check that energy is non-increasing (decreasing for damped system)."""
    x, v = y[0], y[1]
    k = params['k']
    c = params['c']
    m = params['m']
    
    current_energy = 0.5 * m * v**2 + 0.5 * k * x**2
    
    previous_state = kwargs.get('previous_state')
    if previous_state is None:
        return True  # First check, no previous value
    
    prev_x, prev_v = previous_state[0], previous_state[1]
    previous_energy = 0.5 * m * prev_v**2 + 0.5 * k * prev_x**2
    
    # Energy should decrease (or stay same) for damped system
    # Allow small numerical errors
    return current_energy <= previous_energy + 1e-10


def analytical_solution(t, x0, v0, k, c, m):
    """
    Analytical solution for underdamped case (c^2 < 4km).
    
    For underdamped: x(t) = e^(-γt) * [A*cos(ωd*t) + B*sin(ωd*t)]
    where γ = c/(2m), ω0 = sqrt(k/m), ωd = sqrt(ω0^2 - γ^2)
    """
    gamma = c / (2 * m)
    omega0 = np.sqrt(k / m)
    omega_d = np.sqrt(omega0**2 - gamma**2)
    
    # Initial conditions determine A and B
    A = x0
    B = (v0 + gamma * x0) / omega_d
    
    x = np.exp(-gamma * t) * (A * np.cos(omega_d * t) + B * np.sin(omega_d * t))
    v = np.exp(-gamma * t) * (
        -gamma * (A * np.cos(omega_d * t) + B * np.sin(omega_d * t)) +
        omega_d * (-A * np.sin(omega_d * t) + B * np.cos(omega_d * t))
    )
    
    return x, v


if __name__ == "__main__":
    # Simulation parameters
    params = {
        'k': 1.0,   # Spring constant
        'c': 0.1,   # Damping coefficient (underdamped: c^2 < 4km)
        'm': 1.0    # Mass
    }
    
    # Initial conditions: start at x=1, v=0
    y0 = np.array([1.0, 0.0])
    
    # Time span
    t_span = (0.0, 10.0)
    
    print("Running traced simulation of damped harmonic oscillator...")
    print(f"Parameters: k={params['k']}, c={params['c']}, m={params['m']}")
    print(f"Initial state: x={y0[0]}, v={y0[1]}")
    print(f"Time span: {t_span[0]} to {t_span[1]} seconds\n")
    
    # Run traced simulation
    result = trace_run(
        simulate=damped_oscillator,
        params=params,
        t_span=t_span,
        y0=y0,
        invariants=[finite_check, bound_check, energy_decreasing],
        method='RK45',
        evidence_dir='./evidence/damped_oscillator',
        seed=42,
        rtol=1e-8,
        atol=1e-10
    )
    
    print(f"✓ Simulation completed successfully: {result.success}")
    print(f"  Function evaluations: {result.nfev}")
    print(f"  Final time: {result.t[-1]:.2f} s")
    print(f"  Final position: {result.y[0, -1]:.6f}")
    print(f"  Final velocity: {result.y[1, -1]:.6f}\n")
    
    # Check invariants
    if result.invariant_log:
        print("Invariant Check Results:")
        for inv in result.invariant_log.get('invariants', []):
            name = inv['name']
            checks = inv['checks']
            violations = inv['violations']
            severity = inv['severity']
            status = "✓" if violations == 0 else "✗"
            print(f"  {status} {name} ({severity}): {violations}/{checks} violations")
        print()
    
    # Compare with analytical solution
    print("Comparing with analytical solution...")
    t_analytical = np.linspace(t_span[0], t_span[1], 100)
    x_analytical, v_analytical = analytical_solution(
        t_analytical, y0[0], y0[1], params['k'], params['c'], params['m']
    )
    
    # Interpolate numerical solution to analytical time points
    from scipy.interpolate import interp1d
    x_numerical = interp1d(result.t, result.y[0, :])(t_analytical)
    v_numerical = interp1d(result.t, result.y[1, :])(t_analytical)
    
    # Calculate errors
    x_error = np.abs(x_numerical - x_analytical)
    v_error = np.abs(v_numerical - v_analytical)
    
    print(f"  Max position error: {np.max(x_error):.2e}")
    print(f"  Max velocity error: {np.max(v_error):.2e}")
    print(f"  RMS position error: {np.sqrt(np.mean(x_error**2)):.2e}")
    print(f"  RMS velocity error: {np.sqrt(np.mean(v_error**2)):.2e}\n")
    
    # Evidence pack information
    if result.evidence_dir:
        print(f"Evidence pack created at: {result.evidence_dir}")
        print("\nEvidence pack contains:")
        print("  - manifest.json: Complete run metadata (environment, parameters, solver config)")
        print("  - run_log.txt: Timestamped execution log")
        print("  - invariants.json: Invariant check results")
        print("  - data/trajectory.csv: Full state history")
        print("  - plots/time_series.png: Time evolution plots")
        print("  - plots/phase_space.png: Phase portrait")
        print("  - report.md: Human-readable summary")
        print("\nTo reproduce this run:")
        print(f"  1. Use the same parameters: {params}")
        print(f"  2. Use the same initial state: {y0}")
        print(f"  3. Use seed={42} (already set in this run)")
        print(f"  4. Check manifest.json for Python version and package versions")
        print(f"  5. Check git commit in manifest.json (if in git repo)")
    
    print("\n✓ Example complete!")

