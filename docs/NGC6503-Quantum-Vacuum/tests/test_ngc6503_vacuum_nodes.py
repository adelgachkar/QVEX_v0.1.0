"""
Validation Tests for QVEX NGC 6503 Quantum Vacuum & PID Control Nodes.
Author: Adel Gachkar
Target System: NGC 6503 (SPARC Database)

Node 01 is verified against its own source of truth: the LaTeX equation is parsed
out of `nodes_analysis/01_Vacuum_Popcorn_Density_Node.md` and evaluated numerically,
so editing the node without updating the reference implementation (or vice versa)
fails these tests instead of passing silently.
"""

import re
from pathlib import Path

import numpy as np
import pytest

NODE_01_PATH = (
    Path(__file__).resolve().parents[1]
    / "nodes_analysis"
    / "01_Vacuum_Popcorn_Density_Node.md"
)

# ==========================================
# Analytical Models extracted from Nodes
# ==========================================

def rho_popcorn(r, rho_0=1.0, lambda_coh=12.0, gamma_vac=1.0, r_cutoff=50.0):
    """01_Vacuum_Popcorn_Density_Node formulation."""
    return rho_0 * ((1.0 + (r / lambda_coh)) ** (-gamma_vac)) * np.exp(-r / r_cutoff)

def foam_friction(r):
    """02_Nonlinear_Foam_Friction_Node formulation."""
    r = np.asarray(r, dtype=float)
    term1 = 1.1 * np.log(1.0 + (r / 4.5)) * (1.0 - np.exp(-r / 12.0))
    term2 = -0.12 * np.maximum(0.0, r - 4.5)
    return term1 + term2

def pid_control_signal(e, e_int, e_diff, kp=0.92, ki=0.35, kd=0.18):
    """03_PID_Controller_Dynamic_Tuning_Node formulation."""
    return (kp * e) + (ki * e_int) + (kd * e_diff)

def dipole_potential(r, theta, mass=1.0, g=1.0, alpha_dipole=0.05, p_jet=1.0):
    """04_Dipole_Axis_Constraint_Node formulation."""
    r_safe = np.maximum(r, 1e-4)
    v_newton = - (g * mass) / r_safe
    v_dipole = (alpha_dipole * p_jet / (r_safe ** 3)) * (np.cos(theta) ** 2)
    return v_newton + v_dipole


# ==========================================
# Node 01 loader: read + evaluate the node itself
# ==========================================

# LaTeX symbol -> Python identifier, applied before any structural rewriting.
_SYMBOL_MAP = (
    (r"\\rho_\{\\text\{popcorn\}\}", "rho"),
    (r"\\rho_0", "rho_0"),
    (r"\\lambda_\{\\text\{coh\}\}", "lambda_coh"),
    (r"\\gamma_\{\\text\{vac\}\}", "gamma_vac"),
    (r"R_\{\\text\{cutoff\}\}", "r_cutoff"),
)

_SAFE_NAMES = {
    "exp": np.exp,
    "log": np.log,
    "sqrt": np.sqrt,
    "maximum": np.maximum,
    "minimum": np.minimum,
    "abs": np.abs,
}

_FUNCTION_CALLS = ("exp", "log", "sqrt", "maximum", "minimum", "abs")


def load_node_01_text():
    """Return the raw markdown of Node 01 — the artifact under test."""
    assert NODE_01_PATH.is_file(), f"Node 01 is missing at {NODE_01_PATH}"
    return NODE_01_PATH.read_text(encoding="utf-8")


def node_01_formula_expression(text):
    """Extract Node 01's display equation and translate it into a Python expression."""
    blocks = re.findall(r"\$\$(.+?)\$\$", text, flags=re.S)
    assert blocks, "Node 01 must contain a $$ ... $$ display equation"

    formula = next((b for b in blocks if "\\rho" in b), None)
    assert formula is not None, "Node 01 contains no density equation (no \\rho ... $$ block)"
    assert "=" in formula, f"Node 01 equation has no '=' sign: {formula!r}"

    expr = formula.split("=", 1)[1].strip()

    for pattern, replacement in _SYMBOL_MAP:
        expr = re.sub(pattern, replacement, expr)

    expr = expr.replace("\\left", "").replace("\\right", "")
    expr = expr.replace("\\cdot", "*")
    expr = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"((\1)/(\2))", expr)
    expr = re.sub(r"\\exp", "exp", expr)
    expr = re.sub(r"\^\{([^{}]+)\}", r"**(\1)", expr)
    expr = expr.replace("{", "").replace("}", "")

    assert "\\" not in expr, f"Untranslated LaTeX left in Node 01 equation: {expr!r}"

    # Implicit multiplication: "A (B)" -> "A * (B)" and "(...)" juxtaposed with a name.
    expr = re.sub(r"\)\s*(?=[a-zA-Z_(])", ") * ", expr)
    expr = re.sub(
        r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(",
        lambda m: f"{m.group(1)}(" if m.group(1) in _FUNCTION_CALLS else f"{m.group(1)} * (",
        expr,
    )

    expr = re.sub(r"\s+", "", expr)
    assert expr, "Node 01 equation translated to an empty expression"
    return expr


def documented_parameters(text):
    """Parse the parameter values that Node 01 documents in its 'where:' list."""

    def search(pattern, label):
        match = re.search(pattern, text)
        assert match, f"Node 01 must document {label} (pattern: {pattern})"
        return match

    mantissa = search(r"\\rho_0\s*=\s*([0-9.]+)\s*\\times\s*10\^\{(-?\d+)\}", "rho_0")
    rho_0 = float(mantissa.group(1)) * 10.0 ** int(mantissa.group(2))

    lambda_coh = search(r"\\lambda_\{\\text\{coh\}\}\s*=\s*([0-9.]+)", "lambda_coh")
    gamma_vac = search(r"\\gamma_\{\\text\{vac\}\}\s*=\s*([0-9.]+)", "gamma_vac")
    r_cutoff = search(r"R_\{\\text\{cutoff\}\}\s*=\s*([0-9.]+)", "r_cutoff")

    return {
        "rho_0": rho_0,
        "lambda_coh": float(lambda_coh.group(1)),
        "gamma_vac": float(gamma_vac.group(1)),
        "r_cutoff": float(r_cutoff.group(1)),
    }


def node_01_density(r, params):
    """Evaluate Node 01's own equation, as written in the markdown, at radii r."""
    expr = node_01_formula_expression(load_node_01_text())
    namespace = dict(_SAFE_NAMES)
    namespace.update(params)
    namespace["r"] = np.asarray(r, dtype=float)
    return eval(expr, {"__builtins__": {}}, namespace)  # noqa: S307 - repo-local doc input


# ==========================================
# Test Suite
# ==========================================

COMPLETE_ANALYSIS_PATH = Path(__file__).resolve().parents[1] / "NGC6503_QVEX_Complete_Analysis.md"


def rho_equation(text, source):
    """Return the whitespace-normalised rho display equation of a document."""
    blocks = re.findall(r"\$\$(.+?)\$\$", text, flags=re.S)
    equation = next((b for b in blocks if "\\rho" in b), None)
    assert equation is not None, f"{source} contains no \\rho display equation ($$ ... $$)"
    return re.sub(r"\s+", "", equation)


def test_node01_matches_complete_analysis_report():
    """Node 01 and the complete analysis report must state the identical equation."""
    node_equation = rho_equation(load_node_01_text(), "Node 01")

    assert COMPLETE_ANALYSIS_PATH.is_file(), f"Complete analysis is missing at {COMPLETE_ANALYSIS_PATH}"
    report_equation = rho_equation(
        COMPLETE_ANALYSIS_PATH.read_text(encoding="utf-8"), "Complete Analysis"
    )

    assert node_equation == report_equation, (
        "Node 01 and NGC6503_QVEX_Complete_Analysis.md have drifted apart:\n"
        f"  node : {node_equation}\n"
        f"  report: {report_equation}"
    )


def test_node01_documented_parameters():
    """The parameters written in Node 01 must be the ones the codebase actually uses."""
    params = documented_parameters(load_node_01_text())

    assert np.isclose(params["rho_0"], 7.02e-30), "rho_0 must remain the documented physical constant"
    assert np.isclose(params["lambda_coh"], 12.0), "lambda_coh must equal 12.0 kpc"
    assert np.isclose(params["gamma_vac"], 1.0), "gamma_vac must equal the tested falloff index 1.0"
    assert np.isclose(params["r_cutoff"], 50.0), "r_cutoff must equal the tested cutoff 50.0 kpc"

    # The shape parameters documented in the node are the reference implementation's defaults.
    reference_defaults = {"rho_0": 1.0, "lambda_coh": 12.0, "gamma_vac": 1.0, "r_cutoff": 50.0}
    for name in ("lambda_coh", "gamma_vac", "r_cutoff"):
        assert np.isclose(params[name], reference_defaults[name]), (
            f"{name}: Node 01 documents {params[name]} but rho_popcorn() defaults to "
            f"{reference_defaults[name]}"
        )


def test_popcorn_vacuum_density_node():
    """Node 01's equation, parsed from the markdown, must reproduce rho_popcorn exactly."""
    params = documented_parameters(load_node_01_text())
    radii = np.linspace(0.0, 20.0, 201)

    node_curve = node_01_density(radii, params)
    reference_curve = rho_popcorn(radii, **params)

    assert np.allclose(node_curve, reference_curve, rtol=1e-12, atol=0.0), (
        "Node 01's formula no longer matches tests/test_ngc6503_vacuum_nodes.py::rho_popcorn"
    )

    # Scale-free comparison against the reference implementation's normalized defaults.
    assert np.allclose(node_curve / params["rho_0"], rho_popcorn(radii), rtol=1e-12)

    # Physical behaviour of the profile itself.
    assert np.isclose(node_curve[0], params["rho_0"]), "Core density should match base density rho_0"
    assert np.all(node_curve > 0.0), "Vacuum density must remain strictly positive"
    assert np.all(np.diff(node_curve) < 0.0), "Vacuum density must decrease monotonically outward"
    assert node_curve[-1] < 0.5 * params["rho_0"], "Outer disk density must fall well below rho_0"


def test_nonlinear_foam_friction_node():
    """Verify inner coupling and outer damping behavior."""
    f_center = foam_friction(0.0)
    f_transition = foam_friction(4.5)
    f_edge = foam_friction(15.0)

    assert np.isclose(f_center, 0.0), "Friction at absolute center must be zero"
    assert f_transition > 0.0, "Friction inside transition radius must be positive"
    assert f_edge < f_transition, "Outer damping must kick in past transition radius"


def test_pid_controller_tuning_node():
    """Verify optimized PID gains and control signal response."""
    kp, ki, kd = 0.92, 0.35, 0.18
    error = 10.0
    error_integral = 5.0
    error_derivative = -2.0

    signal = pid_control_signal(error, error_integral, error_derivative, kp, ki, kd)
    expected_signal = (0.92 * 10.0) + (0.35 * 5.0) + (0.18 * -2.0)

    assert np.isclose(signal, expected_signal), "PID control calculation mismatch"
    assert signal > 0.0, "Restoring control signal must be positive for positive error"


def test_dipole_axis_constraint_node():
    """Verify axial symmetry breaking under central black hole influence."""
    r_test = 5.0
    v_pole = dipole_potential(r_test, theta=0.0)
    v_equator = dipole_potential(r_test, theta=np.pi / 2.0)

    assert v_pole > v_equator, "Polar potential should have positive dipole jet contribution"
    assert np.isclose(v_equator, -1.0 / r_test), "Equatorial plane should reduce to standard potential"
