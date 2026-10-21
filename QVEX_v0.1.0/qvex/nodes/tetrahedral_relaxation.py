"""
Tetrahedral Relaxation Node for QVEX framework.
Models exponential decay of frustrated lattice stress toward static equilibrium.
"""

from typing import Any, Dict
import math
from qvex.nodes.base import Node


class TetrahedralRelaxationNode(Node):
    """
    Simulates dynamic tetrahedral stress relaxation:
    d(sigma)/dt = -gamma * (sigma - sigma_target)
    """

    def __init__(self, node_id: str, config: Dict[str, Any] = None):
        super().__init__(node_id=node_id, config=config)
        self.relaxation_rate = float(self.config.get("relaxation_rate", 0.5))
        self.dt = float(self.config.get("dt", 0.1))

    def compute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        if "frustration_stress" not in inputs:
            raise ValueError(f"[{self.node_id}] Missing required input 'frustration_stress'.")

        target_stress = float(inputs["frustration_stress"])
        initial_stress = float(inputs.get("initial_stress", target_stress))
        n_steps = int(inputs.get("n_steps", 100))
        gamma = float(self.config.get("relaxation_rate", self.relaxation_rate))
        dt = float(self.config.get("dt", self.dt))

        stress_trace = []
        for step in range(n_steps + 1):
            t = step * dt
            sigma_t = target_stress + (initial_stress - target_stress) * math.exp(-gamma * t)
            stress_trace.append(sigma_t)

        final_stress = stress_trace[-1]

        delta_init = abs(initial_stress - target_stress)
        delta_final = abs(final_stress - target_stress)
        if delta_init > 1e-12:
            eq_ratio = 1.0 - (delta_final / delta_init)
        else:
            eq_ratio = 1.0

        residual_frustration = delta_final

        return {
            "dynamic_stress": final_stress,
            "stress_trace": stress_trace,
            "frustration_stress": target_stress,
            "target_stress": target_stress,
            "initial_stress": initial_stress,
            "relaxation_rate": gamma,
            "equilibrium_ratio": eq_ratio,
            "residual_frustration": residual_frustration,
        }
