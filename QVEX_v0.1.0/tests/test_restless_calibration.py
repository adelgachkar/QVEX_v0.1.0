"""
Tests for Restless Calibration Node (QVEX v0.1.0)
"""

import pytest
from qvex.registry import create_node, register_node
from qvex.nodes.restless_calibration import RestlessCalibrationNode

def test_restless_xor_reclassification():
    config = {
        "tau_circ": 1e-6,
        "tau_meas": 2e-6,
        "tau_delay": 0.53e-6,
        "dynamic_rate": True
    }
    node = RestlessCalibrationNode(node_id="rest_test_1", config=config)
    
    inputs = {
        "memory": [0, 1, 0, 1, 1, 0, 1, 0, 0],
        "circuit_ids": ["c0", "c0", "c0", "c1", "c1", "c1", "c0", "c1", "c0"]
    }
    
    result = node.compute(inputs)
    
    assert result["status"] == "success"
    expected_reclass = [None, 1, 1, 1, 0, 1, 1, 1, 0]
    assert result["reclassified_memory"] == expected_reclass
    assert "c0" in result["counts"]
    assert "c1" in result["counts"]
    assert result["runtime_seconds"] > 0

def test_registry_creation():
    register_node("restless_calibration")(RestlessCalibrationNode)
    node = create_node("restless_calibration", node_id="rest_reg_1", dynamic_rate=False)
    assert node is not None
    assert node.node_id == "rest_reg_1"
    
    res = node.compute({"memory": [0, 1], "circuit_ids": ["a", "a"]})
    assert res["status"] == "success"
    assert node.config.get("dynamic_rate") is False or getattr(node, "dynamic_rate", None) is False
