"""
Reproducibility contract for phytrace.

This module defines explicit guarantees about what phytrace captures and
what it can and cannot guarantee for reproducibility.
"""

from typing import Any, Dict, List


class ReproducibilityContract:
    """
    Explicit contract defining what phytrace guarantees for reproducibility.
    
    This contract makes clear what is captured, what is best-effort, and
    what is explicitly NOT guaranteed. This helps users understand the
    limitations and set appropriate expectations.
    
    Attributes:
        captured: What is automatically captured and stored
        best_effort: What is attempted but may not always succeed
        not_guaranteed: What is explicitly NOT guaranteed
        limitations: Known limitations that affect reproducibility
    """
    
    def __init__(self):
        """Initialize the reproducibility contract."""
        self.captured = {
            "python_version": "Python version and implementation (e.g., CPython 3.11.5)",
            "package_versions": "Versions of key packages (numpy, scipy, matplotlib)",
            "system_info": "OS, architecture, hostname",
            "simulation_parameters": "All parameters passed to trace_run()",
            "initial_state": "Initial state vector y0",
            "solver_config": "Solver method and configuration (method, rtol, atol, etc.)",
            "random_seed": "Seed value used for random number generators",
            "seed_status": "Which RNG libraries had seeds successfully set",
            "git_state": "Git commit hash, branch, and dirty flag (if in git repo)",
            "timestamp": "ISO 8601 timestamp of execution",
            "invariant_definitions": "All invariants checked and their severities",
            "invariant_results": "Violation counts and check statistics",
            "solver_statistics": "Function evaluations, Jacobian evaluations, etc.",
            "trajectory_data": "Complete state trajectory at solver time points",
        }
        
        self.best_effort = {
            "git_repository": "Git info only captured if gitpython is installed and repo exists",
            "package_versions": "Only key packages are captured; sub-dependencies may vary",
            "system_environment": "Environment variables and system-level configs not captured",
            "exact_bit_reproducibility": "Floating-point results may vary across architectures/compilers",
            "external_dependencies": "Third-party libraries called by your simulate() function are not tracked",
        }
        
        self.not_guaranteed = {
            "determinism_across_architectures": "Different CPU architectures may produce slightly different results",
            "determinism_across_compilers": "Different NumPy/SciPy builds may have different numerical results",
            "determinism_with_external_calls": "If simulate() calls external APIs, databases, or non-deterministic code, results will vary",
            "exact_memory_reproducibility": "Memory layout and allocation order are not controlled",
            "thread_safety": "Concurrent calls to trace_run() may interfere with seed management",
            "real_time_guarantees": "No guarantees about execution time or real-time performance",
            "formal_correctness": "Invariants are runtime diagnostics, not formal proofs",
            "certification": "This tool does not provide regulatory certification or compliance guarantees",
        }
        
        self.limitations = [
            "Seeds are set globally; concurrent simulations may interfere",
            "Only captures environment at execution time; system changes between runs are not tracked",
            "Does not capture changes to source code of simulate() function between runs",
            "Floating-point arithmetic is inherently non-deterministic across different hardware",
            "Solver tolerances (rtol, atol) affect numerical precision and may vary",
            "Invariant violations indicate potential issues but do not prove correctness or incorrectness",
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert contract to dictionary for serialization.
        
        Returns:
            Dictionary representation of the contract
        """
        return {
            "captured": self.captured,
            "best_effort": self.best_effort,
            "not_guaranteed": self.not_guaranteed,
            "limitations": self.limitations,
        }
    
    def to_markdown(self) -> str:
        """Convert contract to Markdown format for documentation.
        
        Returns:
            Markdown-formatted contract
        """
        lines = [
            "# Reproducibility Contract",
            "",
            "This document explicitly defines what `phytrace` guarantees for reproducibility.",
            "",
            "## What is Captured",
            "",
        ]
        
        for key, description in self.captured.items():
            lines.append(f"- **{key.replace('_', ' ').title()}**: {description}")
        
        lines.extend([
            "",
            "## Best-Effort (May Not Always Succeed)",
            "",
        ])
        
        for key, description in self.best_effort.items():
            lines.append(f"- **{key.replace('_', ' ').title()}**: {description}")
        
        lines.extend([
            "",
            "## What is NOT Guaranteed",
            "",
        ])
        
        for key, description in self.not_guaranteed.items():
            lines.append(f"- **{key.replace('_', ' ').title()}**: {description}")
        
        lines.extend([
            "",
            "## Known Limitations",
            "",
        ])
        
        for limitation in self.limitations:
            lines.append(f"- {limitation}")
        
        return "\n".join(lines)
    
    def get_summary(self) -> str:
        """Get a one-sentence summary of the contract.
        
        Returns:
            Brief summary statement
        """
        return (
            "phytrace captures execution environment, parameters, seeds, and results "
            "to enable reproducibility, but cannot guarantee exact bit-for-bit "
            "reproducibility across different architectures or when external "
            "non-deterministic code is involved."
        )


# Global contract instance
REPRODUCIBILITY_CONTRACT = ReproducibilityContract()


def get_reproducibility_contract() -> ReproducibilityContract:
    """Get the global reproducibility contract.
    
    Returns:
        ReproducibilityContract instance
    """
    return REPRODUCIBILITY_CONTRACT

