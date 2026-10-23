"""
Regression guards for project integrity (QVEX v0.1.0 technical review).

Each test locks one previously discovered defect:

1. Circular import between ``qvex.registry`` and ``qvex.nodes``:
   importing ``qvex.registry`` first used to fail with ``ImportError``
   (``register_node`` unavailable during partial initialisation).
2. ``five_tetrahedral_union`` registering a passthrough stub even though the
   canonical ``FiveTetrahedralUnionNode`` ships in ``qvex.nodes.tetrahedral_cluster``.
3. ``qvex/core.py`` shadowing the ``qvex/core/`` package.
4. Empty ``CITATION.cff``.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _run_python(code: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-c", code],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )


def test_import_qvex_registry_no_circular_import():
    """`import qvex.registry` must work regardless of import order."""
    proc = _run_python("import sys; sys.path.insert(0, '.'); import qvex.registry; print('ok')")
    assert proc.returncode == 0, proc.stderr
    assert "ok" in proc.stdout

    proc = _run_python(
        "import sys; sys.path.insert(0, '.')\n"
        "import qvex.nodes\n"
        "import qvex.registry\n"
        "import qvex.core.registry\n"
        "print('ok')"
    )
    assert proc.returncode == 0, proc.stderr
    assert "ok" in proc.stdout


def test_builtin_nodes_registered():
    """All shipped node types must be present in the registry."""
    sys.path.insert(0, str(PROJECT_ROOT))
    from qvex.registry import registered_types

    types = registered_types()
    for expected in (
        "cavity_resonator",
        "berry_torque_bridge",
        "peristaltic_pump",
        "boundary_stress_integrator",
        "effective_metric_source",
        "gravitational_curvature",
        "dynamic_inter_cavity_coupler",
        "restless_calibration",
        "five_tetrahedral_union",
    ):
        assert expected in types, f"missing registered type: {expected}"
    assert len(types) >= 14, f"expected >=14 node types, got {len(types)}"


def test_five_tetrahedral_union_is_canonical_implementation():
    """The registry must expose the real class, not the passthrough stub."""
    sys.path.insert(0, str(PROJECT_ROOT))
    from qvex.registry import registered_types

    cls = registered_types()["five_tetrahedral_union"]
    assert "tetrahedral_cluster" in cls.__module__, (
        f"five_tetrahedral_union resolved to stub/legacy module: {cls.__module__}"
    )


def test_example_pipeline_loads_and_executes_end_to_end():
    """The shipped example pipeline must load via the registry and run."""
    proc = _run_python(
        "import sys; sys.path.insert(0, '.')\n"
        "from qvex.registry import load_graph_from_json\n"
        "graph = load_graph_from_json('config/pipeline_qvex_example.json')\n"
        "outputs = graph.run()\n"
        "assert set(outputs) == set(graph.nodes), (sorted(outputs), sorted(graph.nodes))\n"
        "print('ok')"
    )
    assert proc.returncode == 0, proc.stderr
    assert "ok" in proc.stdout


def test_no_shadowing_core_module_beside_package():
    """`qvex/core.py` must not exist next to the `qvex/core/` package."""
    assert not (PROJECT_ROOT / "qvex" / "core.py").exists(), (
        "qvex/core.py shadows the qvex.core package and must be removed"
    )


def test_citation_cff_not_empty():
    """CITATION.cff must carry valid, non-empty citation metadata."""
    text = (PROJECT_ROOT / "CITATION.cff").read_text(encoding="utf-8").strip()
    assert text, "CITATION.cff is empty"
    assert "cff-version:" in text
    assert "Gachkar" in text
