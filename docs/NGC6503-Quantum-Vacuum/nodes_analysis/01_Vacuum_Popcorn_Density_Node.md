---
title: "Node 01: Vacuum Popcorn Density and Zero-Point Fluctuations"
author: "Adel Gachkar"
project: "QVEX-NGC6503-Quantum-Vacuum"
date: "2026-10-26"
tags: [Vacuum_Density, Popcorn_Foam, QuantumVacuum, NGC6503]
---

# Node 01: Vacuum Popcorn Density and Zero-Point Fluctuations

## Overview

This node establishes the foundational vacuum energy density distribution governing the outer boundaries of spiral galaxies, specifically targeting NGC 6503 within the QVEX framework.

## Mathematical Formulation

The local popcorn vacuum energy density $\rho_{\text{popcorn}}(r)$, with $r$ in kpc, is modeled as a fluctuating zero-point field coupled to the baryonic mass distribution:

$$\rho_{\text{popcorn}}(r) = \rho_0 \cdot \left(1 + \frac{r}{\lambda_{\text{coh}}}\right)^{-\gamma_{\text{vac}}} \cdot \exp\left(-\frac{r}{R_{\text{cutoff}}}\right)$$

where:

- $\rho_0 = 7.02 \times 10^{-30} \text{ g/cm}^3$ is the baseline cosmological vacuum density (normalized to `1.0` in the reference implementation).
- $\lambda_{\text{coh}} = 12.0 \text{ kpc}$ represents the quantum vacuum coherence length extracted from SPARC galactic rotation curves.
- $\gamma_{\text{vac}} = 1.0$ is the power-law falloff index.
- $R_{\text{cutoff}} = 50.0 \text{ kpc}$ is the exponential cutoff scale of the popcorn fluctuations.

This is the canonical formulation implemented in `tests/test_ngc6503_vacuum_nodes.py::rho_popcorn` and documented in [[NGC6503_QVEX_Complete_Analysis]] §1. The test suite parses the equation above directly out of this file and evaluates it numerically, so any change to this formula is caught by `PYTHONPATH=. python -m pytest`.

## Physical Interpretation

At galactic boundary scales ($r > 5 \text{ kpc}$), the popcorn vacuum fluctuations provide an emergent attractive stress-energy tensor component that flattens rotation curves without requiring classical dark matter halos.
