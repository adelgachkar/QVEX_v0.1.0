---
title: "Technical Reference & Analytical Note: Independent Validation of NGC 6503 via QVEX Vacuum-Foam Framework"
author: "Adel Gachkar"
affiliation: "Islamic Azad University, Urmia"
orcid: "https://orcid.org/0009-0006-7713-6004"
email: "adelgachkar@gmail.com"
reference_id: "QVEX-REF-NGC6503-2026-V1"
repository: "https://github.com/adelgachkar/QVEX_v0.1.0"
---

## 1. Introduction and Epistemic Separation

This document serves as an independent, citable reference note summarizing the application of the Quantum Vacuum Exchange (QVEX) engine to spiral galaxy NGC 6503. To maintain strict version integrity of the core release (v0.1.0), all empirical SPARC fitting routines (Lelli, McGaugh, & Schombert 2016, AJ, 152, 157), non-linear foam friction derivations, and PID stabilization nodes are documented here as a standalone engineering report.

## 2. Mathematical Formalism of Vacuum-Foam Interaction

The rotation velocity profile flattening of NGC 6503 is modeled without cold dark matter by coupling baryonic mass distributions with a scale-dependent vacuum coherence length ($\lambda_{\text{coh}} = 12.0\text{ kpc}$). The non-linear vacuum friction function governing the outer disk dynamics is defined as:
$$F_{\text{friction}}(r) = 1.1 \cdot \ln\left(1.0 + \frac{r}{4.5}\right) \cdot \left(1.0 - \exp\left(-\frac{r}{12.0}\right)\right) - 0.12 \cdot \max(0, r - 4.5)$$

## 3. PID Feedback Controller & Boundary Stabilization

To eliminate numerical discretization errors and radial oscillation artifacts at the outer boundaries ($r > 15\text{ kpc}$), a closed-loop PID Controller regulates the quantum vacuum density gradient $\eta(r)$:
$$\eta(t) = K_P e(t) + K_I \int e(\tau) d\tau + K_D \frac{de(t)}{dt}$$
The rigorously tuned parameters for NGC 6503 are:

- **Proportional Gain ($K_P$):** $0.92$ (Governing instantaneous restoring stiffness against gravitational potential gradients)

- **Integral Gain ($K_I$):** $0.35$ (Accumulating inward vacuum flux to eliminate steady-state velocity drift)
- **Derivative Gain ($K_D$):** $0.18$ (Providing viscous quantum foam damping along the rotational axis)

## 4. Central Jet Dipole Constraint & Causal Gauge Limits

Disk stability and axial confinement are maintained via opposing relativistic jets establishing a stable potential well along the $\hat{z}$ axis:
$$V_{\text{eff}}(r, \theta) = -\frac{G M(r)}{r} + \frac{\alpha_{\text{dipole}} P_{\text{jet}}}{r^3} \cos^2(\theta)$$

- **Response to Alternative Models ($\Lambda\text{CDM}$ & MOND):** Traditional dark-matter halo models (e.g., NFW) and MOND interpolating functions encounter tensions when addressing localized boundary oscillations and phase-coherent vacuum backreaction. The QVEX framework resolves these discrepancies by interpreting rotation curves through electrodynamic vacuum exchange driven by baryonic currents.

## 5. Verification and Availability

Numerical outputs and fitting routines are verified against empirical SPARC datasets, referencing the benchmark validation plot at `outputs/plots/sparc_ngc6503_fit.png`.

Node-level derivations: [[01_Vacuum_Popcorn_Density_Node|vacuum density]], [[02_Nonlinear_Foam_Friction_Node|foam friction]], [[03_PID_Controller_Dynamic_Tuning_Node|PID tuning]], and [[04_Dipole_Axis_Constraint_Node|dipole-axis constraint]].
