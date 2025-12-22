"""
Double Pendulum Example - Chaotic System

This advanced example demonstrates phytrace with a chaotic system:
the double pendulum. This system exhibits sensitive dependence on initial
conditions, making reproducibility and documentation crucial.

The system has 4 state variables: [θ1, θ2, ω1, ω2]
where θ1, θ2 are angles and ω1, ω2 are angular velocities.

Key challenges:
- Energy conservation (should be constant for undamped case)
- Numerical drift in conserved quantities
- Sensitivity to initial conditions
- Long-term behavior is unpredictable
"""

import numpy as np
from phytrace import trace_run
from phytrace.invariants import finite, create_invariant


def double_pendulum(t, y, m1, m2, L1, L2, g):
    """
    Right-hand side of the double pendulum ODE.
    
    Uses Lagrangian mechanics to derive equations of motion.
    State: [θ1, θ2, ω1, ω2]
    
    Args:
        t: Time
        y: State vector [θ1, θ2, ω1, ω2]
        m1: Mass of first pendulum
        m2: Mass of second pendulum
        L1: Length of first pendulum
        L2: Length of second pendulum
        g: Gravitational acceleration
    
    Returns:
        Derivative [dθ1/dt, dθ2/dt, dω1/dt, dω2/dt]
    """
    theta1, theta2, omega1, omega2 = y
    
    # Intermediate calculations
    delta = theta2 - theta1
    sin_delta = np.sin(delta)
    cos_delta = np.cos(delta)
    
    # Denominators
    denom1 = (m1 + m2) * L1 - m2 * L1 * cos_delta**2
    denom2 = (L2 / L1) * denom1
    
    # Angular accelerations
    alpha1 = (
        m2 * L1 * omega1**2 * sin_delta * cos_delta +
        m2 * g * np.sin(theta2) * cos_delta +
        m2 * L2 * omega2**2 * sin_delta -
        (m1 + m2) * g * np.sin(theta1)
    ) / denom1
    
    alpha2 = (
        -(m2 * L2 * omega2**2 * sin_delta * cos_delta) +
        (m1 + m2) * g * np.sin(theta1) * cos_delta -
        (m1 + m2) * L1 * omega1**2 * sin_delta -
        (m1 + m2) * g * np.sin(theta2)
    ) / denom2
    
    return [omega1, omega2, alpha1, alpha2]


# Energy conservation invariant
# For an undamped double pendulum, total energy should be conserved
@create_invariant(name="energy_conserved", severity="warning")
def energy_conserved(t, y, params, **kwargs):
    """
    Check that total energy is approximately conserved.
    
    Total energy = Kinetic + Potential
    E = T1 + T2 + V1 + V2
    
    For double pendulum:
    T1 = 0.5 * m1 * L1^2 * ω1^2
    T2 = 0.5 * m2 * [L1^2*ω1^2 + L2^2*ω2^2 + 2*L1*L2*ω1*ω2*cos(θ2-θ1)]
    V1 = -m1 * g * L1 * cos(θ1)
    V2 = -m2 * g * [L1*cos(θ1) + L2*cos(θ2)]
    """
    theta1, theta2, omega1, omega2 = y
    m1 = params['m1']
    m2 = params['m2']
    L1 = params['L1']
    L2 = params['L2']
    g = params['g']
    
    delta = theta2 - theta1
    
    # Kinetic energy
    T1 = 0.5 * m1 * L1**2 * omega1**2
    T2 = 0.5 * m2 * (
        L1**2 * omega1**2 +
        L2**2 * omega2**2 +
        2 * L1 * L2 * omega1 * omega2 * np.cos(delta)
    )
    
    # Potential energy
    V1 = -m1 * g * L1 * np.cos(theta1)
    V2 = -m2 * g * (L1 * np.cos(theta1) + L2 * np.cos(theta2))
    
    current_energy = T1 + T2 + V1 + V2
    
    previous_state = kwargs.get('previous_state')
    if previous_state is None:
        return True  # First check
    
    # Calculate previous energy
    prev_theta1, prev_theta2, prev_omega1, prev_omega2 = previous_state
    prev_delta = prev_theta2 - prev_theta1
    
    prev_T1 = 0.5 * m1 * L1**2 * prev_omega1**2
    prev_T2 = 0.5 * m2 * (
        L1**2 * prev_omega1**2 +
        L2**2 * prev_omega2**2 +
        2 * L1 * L2 * prev_omega1 * prev_omega2 * np.cos(prev_delta)
    )
    prev_V1 = -m1 * g * L1 * np.cos(prev_theta1)
    prev_V2 = -m2 * g * (L1 * np.cos(prev_theta1) + L2 * np.cos(prev_theta2))
    
    previous_energy = prev_T1 + prev_T2 + prev_V1 + prev_V2
    
    # Allow small numerical drift (relative error < 1%)
    energy_change = abs(current_energy - previous_energy)
    relative_error = energy_change / (abs(previous_energy) + 1e-10)
    
    return relative_error < 0.01


if __name__ == "__main__":
    # Simulation parameters
    params = {
        'm1': 1.0,   # Mass 1 (kg)
        'm2': 1.0,   # Mass 2 (kg)
        'L1': 1.0,   # Length 1 (m)
        'L2': 1.0,   # Length 2 (m)
        'g': 9.81    # Gravitational acceleration (m/s^2)
    }
    
    print("=" * 70)
    print("Double Pendulum - Chaotic System Example")
    print("=" * 70)
    print("\nThis example demonstrates:")
    print("  1. Multi-dimensional state (4D: θ1, θ2, ω1, ω2)")
    print("  2. Energy conservation tracking")
    print("  3. Sensitivity to initial conditions")
    print("  4. Evidence pack documentation for chaotic systems\n")
    
    # Run 1: Initial condition set 1
    print("Run 1: Initial conditions [θ1=π/2, θ2=π/2, ω1=0, ω2=0]")
    y0_1 = np.array([np.pi/2, np.pi/2, 0.0, 0.0])
    
    result1 = trace_run(
        simulate=double_pendulum,
        params=params,
        t_span=(0.0, 10.0),
        y0=y0_1,
        invariants=[finite(), energy_conserved],
        method='RK45',
        evidence_dir='./evidence/double_pendulum_run1',
        seed=42,
        rtol=1e-8,
        atol=1e-10
    )
    
    print(f"  ✓ Completed: {result1.nfev} function evaluations")
    if result1.invariant_log:
        for inv in result1.invariant_log.get('invariants', []):
            if inv['name'] == 'energy_conserved':
                print(f"  Energy conservation: {inv['violations']}/{inv['checks']} violations")
    
    # Run 2: Slightly different initial conditions
    print("\nRun 2: Initial conditions [θ1=π/2+0.01, θ2=π/2, ω1=0, ω2=0]")
    print("        (Only 0.01 rad difference in θ1)")
    y0_2 = np.array([np.pi/2 + 0.01, np.pi/2, 0.0, 0.0])
    
    result2 = trace_run(
        simulate=double_pendulum,
        params=params,
        t_span=(0.0, 10.0),
        y0=y0_2,
        invariants=[finite(), energy_conserved],
        method='RK45',
        evidence_dir='./evidence/double_pendulum_run2',
        seed=42,
        rtol=1e-8,
        atol=1e-10
    )
    
    print(f"  ✓ Completed: {result2.nfev} function evaluations")
    if result2.invariant_log:
        for inv in result2.invariant_log.get('invariants', []):
            if inv['name'] == 'energy_conserved':
                print(f"  Energy conservation: {inv['violations']}/{inv['checks']} violations")
    
    # Compare trajectories
    print("\n" + "=" * 70)
    print("Trajectory Comparison")
    print("=" * 70)
    
    # Calculate divergence
    # Interpolate to common time points
    from scipy.interpolate import interp1d
    t_common = np.linspace(0, 10, 1000)
    
    theta1_1 = interp1d(result1.t, result1.y[0, :])(t_common)
    theta1_2 = interp1d(result2.t, result2.y[0, :])(t_common)
    
    divergence = np.abs(theta1_1 - theta1_2)
    
    print(f"\nInitial difference: {np.abs(y0_1[0] - y0_2[0]):.6f} rad")
    print(f"Final difference: {divergence[-1]:.6f} rad")
    print(f"Max divergence: {np.max(divergence):.6f} rad")
    print(f"\nThis demonstrates sensitive dependence on initial conditions -")
    print(f"a tiny change in initial state leads to large differences later.")
    
    # Evidence pack benefits
    print("\n" + "=" * 70)
    print("Evidence Pack Benefits for Chaotic Systems")
    print("=" * 70)
    print("\n1. Documenting Equations:")
    print("   - manifest.json records the exact function used")
    print("   - Source code location is captured")
    print("   - Parameters are fully documented")
    
    print("\n2. Tracking Numerical Drift:")
    print("   - Energy conservation violations are logged")
    print("   - Helps identify when numerical errors accumulate")
    print("   - Can compare drift across different solvers")
    
    print("\n3. Reproducibility Despite Chaos:")
    print("   - Same seed ensures same numerical trajectory")
    print("   - Environment capture ensures same packages")
    print("   - Can exactly reproduce 'chaotic' results")
    print("   - Evidence pack proves the simulation was deterministic")
    
    if result1.evidence_dir:
        print(f"\nEvidence packs created at:")
        print(f"  - {result1.evidence_dir}")
        print(f"  - {result2.evidence_dir}")
        print("\nCompare the manifest.json files to see:")
        print("  - Identical parameters and solver settings")
        print("  - Only difference: initial_state values")
        print("  - Same seed ensures deterministic numerical integration")
    
    print("\n✓ Example complete!")
    print("\nNote: For longer simulations, energy drift may become significant.")
    print("      Consider using symplectic integrators for better energy conservation.")

