"""
Dynamic Inter-Cavity Coupler Node for QVEX Framework.
Models time-dependent coupling g(t) between adjacent photonic crystal nanobeam cavities,
computing mode splitting, effective coupling, Rabi exchange rate, and transfer efficiency.
"""

import math
import numpy as np
from typing import Dict, Any, Optional

from qvex.nodes.base import Node
from qvex.registry import register_node


@register_node("dynamic_inter_cavity_coupler")
class DynamicInterCavityCouplerNode(Node):
    """
    Computes mode splitting and energy exchange dynamics between two coupled optical cavities.
    """
    type_name = "dynamic_inter_cavity_coupler"

    def __init__(self, name: Optional[str] = None, node_id: Optional[str] = None, **config):
        super().__init__(name=name, node_id=node_id, **config)
        self.g0 = float(config.get("g0", 1.0e9))  # Default base coupling 1 GHz in rad/s or frequency unit
        self.modulation_depth = float(config.get("modulation_depth", 0.0))
        self.modulation_freq = float(config.get("modulation_freq", 1.0e8))
        self.g_profile = config.get("g_profile", "constant")  # 'constant', 'sin', 'gaussian_pulse'
        self.pulse_sigma = float(config.get("pulse_sigma", 1.0e-6))
        self.pulse_center = float(config.get("pulse_center", 0.0))

    def compute(self, inputs: Dict[str, Any], *args, **kwargs) -> Dict[str, Any]:
        # 1. Extract frequencies and parameters with fallback defaults
        omega1 = float(inputs.get("omega1", inputs.get("frequency_ghz_1", 6.0) * 2.0 * math.pi * 1e9))
        omega2 = float(inputs.get("omega2", inputs.get("frequency_ghz_2", 6.0) * 2.0 * math.pi * 1e9))
        
        g_base = float(inputs.get("g", inputs.get("g0", self.g0)))
        detuning_input = inputs.get("detuning", inputs.get("detuning_ghz", None))
        if detuning_input is not None:
            delta = float(detuning_input) * (2.0 * math.pi * 1e9 if "ghz" in str(inputs).lower() else 1.0)
        else:
            delta = omega1 - omega2

        # Time grid for dynamic profiles
        dt = float(inputs.get("dt", 1.0e-11))
        n_steps = int(inputs.get("n_steps", 1000))
        t = np.arange(n_steps) * dt

        # 2. Compute dynamic coupling g(t)
        if self.g_profile == "sin":
            g_t = g_base * (1.0 + self.modulation_depth * np.sin(2.0 * math.pi * self.modulation_freq * t))
        elif self.g_profile == "gaussian_pulse":
            g_t = g_base * np.exp(-((t - self.pulse_center) ** 2) / (2.0 * (self.pulse_sigma ** 2)))
        else:  # constant
            g_t = np.full_like(t, g_base)

        g_eff = float(np.sqrt(np.mean(g_t ** 2)))
        g_instant = float(g_t[-1])

        # 3. Eigenfrequencies and Mode Splitting (bonding / anti-bonding)
        # omega_pm = (omega1 + omega2)/2 ± sqrt((delta/2)^2 + g^2)
        mean_omega = 0.5 * (omega1 + omega2)
        radical = math.sqrt((0.5 * delta) ** 2 + g_instant ** 2)
        omega_plus = mean_omega + radical
        omega_minus = mean_omega - radical
        mode_splitting = omega_plus - omega_minus  # 2 * radical

        # 4. Exchange dynamics
        exchange_rate = math.sqrt(delta ** 2 + 4.0 * (g_instant ** 2))
        rabi_period = (2.0 * math.pi / exchange_rate) if exchange_rate > 0.0 else float('inf')
        swap_period_resonant = (math.pi / abs(g_instant)) if abs(g_instant) > 0.0 else float('inf')

        # Estimated transfer efficiency over a swap half-period
        # η = 4g^2 / (delta^2 + 4g^2)
        denom = delta ** 2 + 4.0 * (g_instant ** 2)
        transfer_efficiency_est = (4.0 * (g_instant ** 2) / denom) if denom > 0.0 else 1.0

        return {
            "omega1": omega1,
            "omega2": omega2,
            "delta": delta,
            "g_eff": g_eff,
            "g_instant": g_instant,
            "omega_plus": omega_plus,
            "omega_minus": omega_minus,
            "mode_splitting": mode_splitting,
            "exchange_rate": exchange_rate,
            "rabi_period": rabi_period,
            "swap_period_resonant": swap_period_resonant,
            "transfer_efficiency_est": transfer_efficiency_est,
            "time_trace": {
                "t": t.tolist(),
                "g_t": g_t.tolist()
            }
        }
