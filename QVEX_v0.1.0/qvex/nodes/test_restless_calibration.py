"""
Unit tests for RestlessCalibrationNode in QVEX framework.
"""

import pytest
from qvex.nodes.restless_calibration import RestlessCalibrationNode
from qvex.registry import create_node, clear_registry

def setup_function():
    clear_registry()

def test_restless_xor_reclassification():
    config = {
        "tau_circ": 1.0e-6,
        "tau_meas": 2.0e-6,
        "tau_delay": 0.53e-6,
        "dynamic_rate": True
    }
    node = RestlessCalibrationNode(node_id="restless_test", config=config)
    
    # Example sequence from Tornow et al. Fig. 2
    memory = [0, 1, 0, 1, 1, 0, 1, 0, 0]
    circuit_ids = ["c0", "c0", "c0", "c1", "c1", "c1", "c0", "c1", "c0"]
    
    inputs = {
        "memory": memory,
        "circuit_ids": circuit_ids,
        "n_shots": len(memory)
    }
    
    result = node.compute(inputs)
    
    assert result["status"] == "success"
    # First entry must be None because there is no predecessor
    assert result["reclassified_memory"][0] is None
    # Subsequent entries must match XOR logic
    # [0, 1, 0, 1, 1, 0, 1, 0, 0] -> XOR -> [None, 1, 1, 1, 0, 1, 1, 1, 0]
    assert result["reclassified_memory"][1:] == [1, 1, 1, 0, 1, 1, 1, 0]
    assert "c0" in result["counts"]
    assert "c1" in result["counts"]
    assert result["runtime_seconds"] > 0.0

def test_registry_creation():
    # Test if node can be instantiated via global registry
    node = create_node("restless_calibration", node_id="rest_reg_1", config={"dynamic_rate": False})
    assert node is not None
    assert node.node_id == "rest_reg_1"
    
    res = node.compute({"memory": [1, 0], "circuit_ids": ["a", "a"], "n_shots": 2})
    assert res["status"] == "success"
    assert res["dynamic_rate_active"] is False
