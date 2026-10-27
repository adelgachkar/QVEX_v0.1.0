---
title: "Node 02: Nonlinear Quantum Foam Friction"
author: "Adel Gachkar"
project: "QVEX-NGC6503-Quantum-Vacuum"
date: "2026-10-26"
tags: [Foam_Friction, Dissipation, QuantumVacuum, NGC6503]
---

# Node 02: Nonlinear Quantum Foam Friction

## Overview

This node models the dissipative and resistive drag experienced by test masses traversing the spacetime quantum foam structure at galactic peripheries.

## Mathematical Formulation

The canonical, empirically calibrated radial friction force $F_{\text{friction}}(r)$ (matched to [[QVEX_NGC6503_Technical_Reference]] §2 and `tests/test_ngc6503_vacuum_nodes.py::foam_friction`) is:

$$F_{\text{friction}}(r) = 1.1 \cdot \ln\left(1.0 + \frac{r}{4.5}\right) \cdot \left(1.0 - \exp\left(-\frac{r}{12.0}\right)\right) - 0.12 \cdot \max(0, r - 4.5)$$

with the core–boundary transition at $r = 4.5$ kpc and outer-disk stabilization beyond.

## Conceptual Velocity-Gradient Form

The underlying physical picture can be expressed as a nonlinear damping of orbital velocity gradients,

$$F_{\text{foam}}(v, r) = -\gamma_{\text{foam}} \cdot v(r) \cdot \left| \frac{\partial v}{\partial r} \right|^{\alpha}, \qquad \alpha = 1.5,$$

with $\gamma_{\text{foam}}$ calibrated against MOND acceleration scales ($a_0 = 1.15 \times 10^{-10} \text{ m/s}^2$). **This velocity-gradient expression is a conceptual precursor; the radial model above is the implemented and tested formulation.**

## Damping Mechanism

The nonlinear damping suppresses unphysical velocity divergences at the outer edge of NGC 6503, ensuring asymptotic convergence to the observed flat rotation velocity $v_{\infty} \approx 120 \text{ km/s}$.
