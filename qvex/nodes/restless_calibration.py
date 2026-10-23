"""
Restless Calibration and Dynamic Repetition Rate Node
Inspired by: Tornow et al., "Minimum Quantum Run-Time Characterization 
and Calibration via Restless Measurements with Dynamic Repetition Rates", 
PRX Applied 17, 064061 (2022).
"""

from typing import Dict, Any, List
from .base import Node
from ..registry import register_node

@register_node("restless_calibration")
class RestlessCalibrationNode(Node):
    """
    Implements restless measurement post-processing (sequential XOR filtering 
    m_{j-1} ^ m_j) and dynamic repetition rate runtime characterization 
    for calibration pipelines in the QVEX framework.
    """
    def __init__(self, node_id: str = None, label: str = None, config: Dict[str, Any] = None, name: str = None, **kwargs):
        super().__init__(node_id=node_id, label=label, config=config, name=name, **kwargs)
        self.tau_circ = self.config.get("tau_circ", 0.41e-6)     # Average circuit execution time (seconds)
        self.tau_meas = self.config.get("tau_meas", 5.4e-6)     # Readout measurement time (seconds)
        self.tau_reset = self.config.get("tau_reset", 100.0e-6) # Active reset overhead (seconds)
        self.tau_delay = self.config.get("tau_delay", 1.0e-6)   # Restless classical processing latency (seconds)
        self.dynamic_rate = self.config.get("dynamic_rate", True)

    def compute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        memory = inputs.get("memory", [])
        circuit_ids = inputs.get("circuit_ids", [])
        n_shots = inputs.get("n_shots", len(memory))

        if not memory:
            return {
                "time_ordered_memory": [],
                "reclassified_memory": [],
                "counts": {},
                "runtime_seconds": 0.0,
                "status": "empty_input"
            }

        # 1. Reclassify time-ordered memory using sequential XOR: m_{j-1} ^ m_j
        # Reference: Tornow et al., Fig. 2 (sequential bitwise XOR for restless shots)
        reclassified = [None]  # First shot has no predecessor
        for prev, curr in zip(memory[:-1], memory[1:]):
            reclassified.append(int(prev) ^ int(curr))

        # 2. Group and count results per circuit (ignoring the first None entry)
        counts_per_circuit = {}
        for cid, res in zip(circuit_ids[1:], reclassified[1:]):
            if cid not in counts_per_circuit:
                counts_per_circuit[cid] = {"0": 0, "1": 0}
            counts_per_circuit[cid][str(res)] += 1

        # 3. Calculate runtime based on dynamic repetition rates vs active reset overhead
        # Reference: Tornow et al., Table II & Section IV
        if self.dynamic_rate:
            per_shot_time = self.tau_circ + self.tau_meas + self.tau_delay
        else:
            per_shot_time = self.tau_circ + self.tau_meas + self.tau_reset + self.tau_delay

        total_runtime = n_shots * per_shot_time

        return {
            "time_ordered_memory": memory,
            "reclassified_memory": reclassified,
            "counts": counts_per_circuit,
            "runtime_seconds": total_runtime,
            "dynamic_rate_active": self.dynamic_rate,
            "status": "success"
        }
