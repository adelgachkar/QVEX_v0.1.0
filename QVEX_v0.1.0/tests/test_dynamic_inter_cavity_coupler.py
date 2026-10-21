"""
Unit tests for DynamicInterCavityCouplerNode in QVEX framework.
"""

import math
import pytest
from qvex.nodes.dynamic_inter_cavity_coupler import DynamicInterCavityCouplerNode
from qvex.core.registry import NodeRegistry


def test_coupler_resonant_splitting():
    node = DynamicInterCavityCouplerNode(g0=1e6)
    # Resonant case: omega1 == omega2 -> delta = 0
    res = node.compute({"omega1": 2e9, "omega2": 2e9, "g": 1e6})
    
    assert math.isclose(res["delta"], 0.0, abs_tol=1e-9)
    # Mode splitting should be exactly 2 * g = 2e6
    assert math.isclose(res["mode_splitting"], 2e6, rel_tol=1e-5)
    # Swap period should be pi / g
    expected_swap = math.pi / 1e6
    assert math.isclose(res["swap_period_resonant"], expected_swap, rel_tol=1e-5)
    assert math.isclose(res["transfer_efficiency_est"], 1.0, rel_tol=1e-5)


def test_coupler_detuned_case():
    node = DynamicInterCavityCouplerNode()
    # Detuned case: delta = 4e6, g = 3e6 -> splitting = 2 * sqrt((4e6/2)^2 + (3e6)^2) = 2 * sqrt(4e12 + 9e12) = 2 * sqrt(13e12)
    res = node.compute({"omega1": 10e6, "omega2": 6e6, "g": 3e6})
    
    expected_splitting = 2.0 * math.sqrt((2.0e6)**2 + (3.0e6)**2)
    assert math.isclose(res["mode_splitting"], expected_splitting, rel_tol=1e-5)
    assert res["transfer_efficiency_est"] < 1.0


def test_coupler_sin_profile_rms():
    g0 = 1e6
    mod_depth = 0.5
    node = DynamicInterCavityCouplerNode(g0=g0, modulation_depth=mod_depth, g_profile="sin")
    res = node.compute({"dt": 1e-9, "n_steps": 10000})
    
    # For RMS of g0 * (1 + m * sin(wt)), RMS = g0 * sqrt(1 + m^2 / 2)
    expected_g_eff = g0 * math.sqrt(1.0 + (mod_depth ** 2) / 2.0)
    assert math.isclose(res["g_eff"], expected_g_eff, rel_tol=1e-2)


def test_coupler_registry_integration():
    registry = NodeRegistry()
    registry.register("dynamic_inter_cavity_coupler", DynamicInterCavityCouplerNode)
    
    assert "dynamic_inter_cavity_coupler" in registry.list_nodes()
    node_instance = registry.get("dynamic_inter_cavity_coupler")(g0=5e5)
    assert isinstance(node_instance, DynamicInterCavityCouplerNode)
    
    out = node_instance.compute({"omega1": 1e9, "omega2": 1e9})
    assert "mode_splitting" in out
