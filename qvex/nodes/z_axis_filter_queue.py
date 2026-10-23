"""
Z-Axis Filter Queue Node for QVEX framework.
Filters spatial propagating modes, handles jet flux and intensity,
and limits queue state strictly by queue_capacity.
"""

from typing import Any, Dict, List
import numpy as np
from qvex.nodes.base import Node


class ZAxisFilterQueueNode(Node):
    """
    Filters spatial modes propagating along the z-axis jet cavity,
    maintaining a bounded queue capacity and tracking effective flux and gain.
    """

    def __init__(self, node_id: str, config: Dict[str, Any] = None):
        super().__init__(node_id=node_id, config=config)
        cfg = config or {}
        if hasattr(self, "config") and isinstance(self.config, dict):
            cfg = {**self.config, **cfg}
        self.queue_capacity = int(cfg.get("queue_capacity", 5))
        self.alpha_growth = float(cfg.get("alpha_growth", 0.3))

    def compute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        jet_flux = inputs.get("jet_flux", None)
        intensity = inputs.get("intensity", None)
        screened_phase = inputs.get("screened_phase", 0.0)
        z_steps = inputs.get("z_steps", np.linspace(0.0, 1.0, 10))
        r_wall = float(inputs.get("r_wall", 1.0))
        
        # Read capacity explicitly from config dictionary or instance variable
        cap = int(self.config.get("queue_capacity", self.queue_capacity)) if hasattr(self, "config") else self.queue_capacity

        # Support scalar or list of phases
        if isinstance(screened_phase, (int, float)):
            phase_list = [float(screened_phase)]
        else:
            phase_list = [float(p) for p in screened_phase]

        # Prepare mode amplitudes
        if jet_flux is not None:
            if isinstance(jet_flux, (int, float)):
                modes_input = [float(jet_flux)]
            else:
                modes_input = [float(f) for f in jet_flux]
        elif intensity is not None:
            modes_input = [float(intensity)]
        else:
            modes_input = [1.0]

        z_steps_arr = np.asarray(z_steps, dtype=float)

        # Compute SNR profile along z
        snr_profile = []
        for z in z_steps_arr:
            snr = float(np.exp(-self.alpha_growth * z) / max(r_wall, 1e-6))
            snr_profile.append(snr)

        # Build filtered modes
        filtered_modes = []
        for idx, val in enumerate(modes_input):
            phase = phase_list[idx] if idx < len(phase_list) else phase_list[-1]
            amp = float(val) * (1.0 + self.alpha_growth * 0.5) / max(r_wall, 1e-5)
            filtered_modes.append({
                "mode_idx": idx,
                "amplitude": amp,
                "phase": phase,
            })

        # Sort queue by amplitude descending and truncate strictly to cap
        sorted_modes = sorted(filtered_modes, key=lambda m: m["amplitude"], reverse=True)
        bounded_queue = sorted_modes[:cap]

        effective_axial_flux = float(sum(m["amplitude"] for m in bounded_queue)) if bounded_queue else 0.0
        resonance_gain = float(1.0 + (1.0 / max(r_wall, 0.1)) * (1.0 + self.alpha_growth))

        return {
            "filtered_modes": filtered_modes,
            "snr_profile": snr_profile,
            "z_queue_state": bounded_queue,
            "effective_axial_flux": effective_axial_flux,
            "resonance_gain": resonance_gain,
            "queue_capacity": cap,
        }
