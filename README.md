# QVEX — Quantum Vacuum Exchange Engine

**A modular, DAG-based research scaffold for coupled-cavity photonics,
geometric stress integration, and hypothesis-driven gravity modeling.**

[![CI Tests](https://github.com/adelgachkar/QVEX_v0.1.0/actions/workflows/tests.yml/badge.svg)](https://github.com/adelgachkar/QVEX_v0.1.0/actions/workflows/tests.yml)
![Python 3.10–3.12](https://img.shields.io/badge/python-3.10%E2%80%933.12-blue.svg)
![64 tests](https://img.shields.io/badge/tests-64%20passed-brightgreen.svg)
![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)
[![Citation](https://img.shields.io/badge/citation-CITATION.cff-purple.svg)](CITATION.cff)

---

## Why QVEX?

QVEX lets you **compose physics as a directed acyclic graph (DAG)**: each node is a
self-contained physical hypothesis with typed input/output ports, and a pipeline is a
declarative JSON file. Swap a node, re-run the suite, and see exactly what changed —
no hidden state, no monolithic simulator.

It is built for researchers who want to:

- **Test cavity-photonics ideas quickly** — resonators, dynamic inter-cavity couplers,
  non-Markovian cavities, and optical phase steps with physically meaningful parameters
  (Q-factors, detuning, coupling strength, Lindblad-style damping).
- **Bridge quantum geometry to mechanics** — Berry curvature, geometric (Aharonov–Bohm
  style) torque, quantum backreaction, and resonant spinon zero-modes wired into
  boundary-stress integration and radiation-pressure thrust.
- **Explore gravity hypotheses without dark matter** — tetrahedral angular-deficit
  curvature, popcorn-vacuum nucleation modulation, and observational coupling nodes that
  fit MOND-like acceleration scales against the real SPARC galaxy rotation dataset.
- **Keep claims honest** — every module carries an *epistemic class* (Class A: established
  experiments → Class D: frontier predictions), so collaborators always know what is
  validated, what is a working model, and what is a conjecture under test.

## Highlights

| Capability | What you get |
| :--- | :--- |
| **Pure-Python DAG engine** | Deterministic execution, cycle detection, typed ports — zero runtime dependencies beyond NumPy |
| **20 physics nodes / 14 registry types** | Photonics, quantum geometry, stress integration, curvature, observational coupling, lab benchmarks |
| **JSON pipelines + schema** | Declarative graphs validated by `config/schemas/graph.schema.json`; load with one call |
| **Real-data hooks** | SPARC rotation-curve loader and Eöt-Wash / laboratory Yukawa-bound comparison scripts |
| **Publication figures** | Matplotlib scripts for cavity stress profiles, radial flux, RAR/MOND coupling, lab exclusion plots |
| **64-test suite + CI** | Every node contract, DAG routing, and end-to-end pipeline guarded on Python 3.10–3.12 |
| **Obsidian knowledge vault** | 13 linked theory documents (axiomatic blueprint → Lindblad dynamics → validation framework) browseable as a graph |

## Node Catalog

| Photonics | Quantum Geometry | Mechanics & Gravity | Observation |
| :--- | :--- | :--- | :--- |
| `cavity_resonator` | `berry_torque_bridge` | `boundary_stress_integrator` | `observational_coupling` |
| `non_markovian_cavity` | `quantum_backreaction` | `effective_metric_source` | `laboratory_benchmarks` |
| `dynamic_inter_cavity_coupler` | `optical_phase_step` | `gravitational_curvature` | `restless_calibration` |
| `peristaltic_pump` | `resonant_spinon_zero_mode` | `tetrahedral_cluster` / `five_tetrahedral_union` | — |
| `radial_propagation` | — | `tetrahedral_relaxation` | — |
| `z_axis_filter_queue` | — | `popcorn_vacuum_density` | — |


## Quick Start

```bash
git clone https://github.com/adelgachkar/QVEX_v0.1.0.git
cd QVEX_v0.1.0
python -m pip install -e .          # core (NumPy only)
python -m pip install -e ".[test]"  # + pytest

python -m pytest -q                 # → 64 passed
```

Run the shipped example pipeline end-to-end:

```bash
python -c "from qvex.registry import load_graph_from_json; \
print(sorted(load_graph_from_json('config/pipeline_qvex_example.json').run().keys()))"
# → ['cavity_1', 'cavity_2', 'coupler', 'metric', 'pump', 'stress']
```

Declare your own graph in JSON (validated against the schema), or register a new node
with a single decorator:

```python
from qvex.nodes.base import Node
from qvex.registry import register_node

@register_node("my_hypothesis")
class MyHypothesisNode(Node):
    """EPISTEMIC CLASS: D (differential prediction)."""
    def compute(self, inputs):
        return {"prediction": 42.0}
```

## The Epistemic Contract

QVEX does not ask you to trust it. Each node and document declares where it stands:

| Class | Meaning |
| :--- | :--- |
| **A** — Established | Reproducible laboratory physics (Casimir, Lindblad, Berry phase, Rayleigh–Plesset) |
| **B** — Guaranteed | Algorithmic consistency: unit balance, DAG integrity, the 64-test suite |
| **C** — Working model | Phenomenological analogs under active test (tetrahedral deficit, popcorn vacuum) |
| **D** — Frontier | Differential predictions awaiting observation (field charge from strand geometry) |

See [`docs/10_Epistemic_Stratification_and_Validation_Framework.md`](docs/10_Epistemic_Stratification_and_Validation_Framework.md).

## Documentation Vault

Open the repository folder as an **Obsidian vault** and start at
[`docs/QVEX_Master_Index.md`](docs/QVEX_Master_Index.md) to browse the linked theory
graph: axiomatic blueprint, unit/dimensional concordance, instrument calibration,
de Sitter boundary coupling, quantum Zeno decoherence, multi-cavity Lindblad transfer,
photonic-crystal nanobeam design rules, and the popcorn-vacuum technical report.

## Project Layout

```text
qvex/
├── core/        # DAG engine (graph.py) and node registry (registry.py)
├── nodes/       # 20 physics nodes, one module per pipeline stage
└── data/        # SPARC rotation-curve loader
config/          # Example pipeline JSON + JSON schema
docs/            # Obsidian theory vault (13 documents)
scripts/         # Fitting and publication-figure generators
tests/           # 64 pytest guards (CI on 3.10 / 3.11 / 3.12)
```

## Citation

If QVEX contributes to your work, please cite it using the metadata in
[`CITATION.cff`](CITATION.cff):

> Gachkar, A. (2026). *QVEX — Quantum Vacuum Exchange Engine* (Version 0.1.0) [Software].
> [https://github.com/adelgachkar/QVEX_v0.1.0]

## License

MIT — see [`LICENSE`](LICENSE). The same license is declared in
[`CITATION.cff`](CITATION.cff) and in the Zenodo deposit metadata
(`.zenodo.json`).

## Status & Honest Scope

QVEX is a **computational research scaffold, not a validated physical engine**. All
theoretical constructs, fits, and plots are hypotheses/model outputs — not established
experimental results. Review [`docs/02_Open_Calibration_Checklist.md`](docs/02_Open_Calibration_Checklist.md)
before making empirical claims, and keep every new node labeled with its epistemic class.

## Author

**Adel Gachkar** — Communications Engineer & Quantum ML Researcher,
Islamic Azad University, Urmia · [ORCID 0009-0006-7713-6004](https://orcid.org/0009-0006-7713-6004)

Contributions, issue reports, and physics critiques are welcome.
