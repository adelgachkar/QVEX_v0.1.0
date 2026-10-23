# 08. Photonic-Crystal Nanobeam Cavities and Coupled Modes Analysis

## 1. Bibliographic Metadata
- **Primary source:** *Single and Coupled Nanobeam Cavities* (Chapter 2, *Advances in Photonic Crystals*)
- **Authors:** Aliaksandra M. Ivinskaya, Andrei V. Lavrinenko, Dzmitry M. Shyroki, and Andrey A. Sukhorukov
- **Digital identifier:** DOI: 10.5772/55096
- **Validation status:** Fully validated (Electromagnetic Eigenmode Analysis & Maxwell-based Photonics)

---

## 2. Purpose and Mapping to the QVEX Project
This document transfers the physics of very-high-Q optical cavities ($Q \sim 10^5$) and hybridized coupled-mode analysis into the `QVEX_v0.1.0` simulation framework. These concepts replace the parametric placeholders in the following nodes:
1. `CavityResonatorNode`: determines the true field-loss rate ($\kappa$) and mode quality from the physical hole geometry and beam width.
2. `PeristalticPumpNode`: models the power-transfer matrix between two coupled cavities based on frequency splitting.

---

## 3. Core Formulations and Electromagnetic Foundations

### 3.1. Complex Frequency and Q-factor
Solving Maxwell's equations directly for the electromagnetic eigenmodes yields the complex eigenfrequency $\tilde{\omega} = \omega_r + i\omega_i$. The intrinsic cavity quality factor is then defined as:
$$Q = \frac{\text{Re}(\omega)}{2\,\text{Im}(\omega)} = \frac{\omega_r}{2\gamma}$$
where $\gamma = \text{Im}(\omega)$ is the radiation-loss rate into the unbounded medium, directly related to the Lindblad damping parameter ($\kappa = 2\gamma = \frac{\omega_r}{Q}$) used by the `CavityResonatorNode`.

### 3.2. Coupling of Parallel Cavities and Hybridized Supermodes
When two nanobeams are placed side by side with gap $g$, the electric-field symmetry is broken and two supermodes form:
- **Even mode (symmetric):** the electric field in the gap between the two beams is in phase ($\omega_{\text{even}}$).
- **Odd mode (anti-symmetric):** the electric field between the two beams has a phase difference of $\pi$ ($\omega_{\text{odd}}$).

The frequency splitting is set by the mutual coupling rate $J$:
$$\Delta\omega = \omega_{\text{odd}} - \omega_{\text{even}} \approx 2J$$
This coefficient $J$ is exactly the spatial coupling coefficient between the peristaltic-pump elements of this project.

### 3.3. Longitudinal-Shift Mode Degeneracy
Applying a longitudinal shift $s$ between two parallel nanobeams changes the spatial dependence of the coupling:
- At the critical shift $s \approx 0.4a$ (with $a$ the hole-lattice constant), the frequency splitting tends to zero ($\Delta\omega \to 0$) and **resonant-mode degeneracy** is observed.
- At this degeneracy point the modal $Q$ factors do not drop abruptly, enabling compact, loss-free resonant energy transfer.

---

## 4. Proposed Geometric Parameters for Implementation and Calibration

| Parameter | Physical symbol | Standard SOI range | Effect on the simulation node |
| :--- | :--- | :--- | :--- |
| **Lattice constant** | $a$ | $300\text{ nm} - 450\text{ nm}$ | Sets the central resonance frequency $\omega_0$ |
| **Hole radius** | $r$ | $0.25a - 0.35a$ | Sets the photonic bandgap width |
| **Beam width** | $w$ | $1.0a - 1.5a$ | Controls the mode volume $V_{\text{mode}}$ |
| **Quality factor** | $Q$ | $10^4 - 10^5$ | Sets the `decay_rate` parameter of `CavityResonatorNode` |
| **Nanobeam gap** | $g$ | $100\text{ nm} - 300\text{ nm}$ | Sets the `coupling_strength` parameter of `PeristalticPumpNode` |

---

## 5. Theoretical Scope and Scientific Boundaries
1. **Classical nature of the Maxwell modes:** the phenomena analyzed in this reference are steady-state solutions of the classical Maxwell equations in photonic-crystal nanostructures; they enter QVEX as classical analog parameterizations, not as evidence for quantum-vacuum effects.
