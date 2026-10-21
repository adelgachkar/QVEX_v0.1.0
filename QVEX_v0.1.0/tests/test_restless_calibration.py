import pytest
import numpy as np
import qvex.nodes
from qvex.registry import create_node
from qvex.nodes.restless_calibration import RestlessCalibrationNode


def test_restless_calibration_execution():
    node = RestlessCalibrationNode(
        node_id="rest_1",
        config={"dynamic_rate": True, "base_repetition_rate_hz": 1e5}
    )
    inputs = {
        "memory": ["0", "1", "1", "0"],
        "circuit_ids": [0, 0, 1, 1]
    }
    outputs = node.compute(inputs)
    assert "time_ordered_memory" in outputs
    assert "reclassified_memory" in outputs
    assert "counts" in outputs
    assert "runtime_seconds" in outputs
    assert outputs["runtime_seconds"] >= 0.0


def test_registry_creation():
    node = create_node("restless_calibration", node_id="rest_reg_1", config={"dynamic_rate": False})
    assert isinstance(node, RestlessCalibrationNode)
    assert node.node_id == "rest_reg_1"
