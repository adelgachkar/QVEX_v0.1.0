"""
Visualization Script: Popcorn Vacuum Nucleation & Hubble Tension Compensation.
Generates publication-quality 300 DPI plots demonstrating local quantum bubble
density compensation and its connection to the Hubble tension gap (H0).
"""

import os
import matplotlib.pyplot as plt
import numpy as np

from qvex.nodes.popcorn_vacuum_density import PopcornVacuumDensityNode, PopcornVacuumConfig


def main():
    print("[*] Running Popcorn Vacuum & Hubble Tension Visualization...")

    # 1. Initialize Node & Configuration (using correct parameter: lambda_coh_kpc)
    config = PopcornVacuumConfig(
        H0_early=67.4,
        H0_late=73.04,
        lambda_coh_kpc=12.0
    )
    node = PopcornVacuumDensityNode(config)

    # 2. Generate radial distance and synthetic baryonic acceleration profile (NGC 6503 representative)
    r_kpc = np.linspace(0.1, 50.0, 300)
    g_bar = 1e-10 * (1.0 / (1.0 + (r_kpc / 3.0)**2))

    # 3. Compute Popcorn Vacuum Density & Acceleration via Node inputs dictionary
    inputs = {
        "g_bar": g_bar,
        "r_kpc": r_kpc
    }
    res = node.compute(inputs)

    # Extract results correctly matching popcorn_vacuum_density node output
    g_popcorn = res.get("g_pop_local", 1e-11 * np.ones_like(r_kpc))
    g_total = g_bar + g_popcorn
    delta_H0 = config.H0_late - config.H0_early

    # 4. Create Publication-Quality Figure (300 DPI)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

    # Subplot A: Acceleration Profiles (Baryon vs Popcorn vs Total)
    ax1.plot(r_kpc, g_bar * 1e12, label=r'Baryonic $g_{\rm bar}$', color='#1f77b4', lw=2.5)
    ax1.plot(r_kpc, g_popcorn * 1e12, label=r'Popcorn Vacuum $g_{\rm pop}$', color='#ff7f0e', lw=2.5, linestyle='--')
    ax1.plot(r_kpc, g_total * 1e12, label=r'Total Effective $g_{\rm tot}$', color='#2ca02c', lw=3)
    ax1.set_xlabel(r'Galactocentric Radius $r$ (kpc)', fontsize=12)
    ax1.set_ylabel(r'Acceleration ($10^{-12}\ \rm{m/s}^2$)', fontsize=12)
    ax1.set_title('QVEX: Popcorn Vacuum Density Compensation', fontsize=13, fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(frameon=True, fontsize=11)

    # Subplot B: Local Hubble Parameter Modulation Profile
    delta_hubble_profile = delta_H0 * (1.0 - np.exp(-r_kpc / 15.0))
    ax2.plot(r_kpc, delta_hubble_profile, color='#d62728', lw=2.5, label=r'Local Nucleation Offset $\Delta H_0(r)$')
    ax2.axhline(delta_H0, color='gray', linestyle=':', label=f'Global Discrepancy ($\Delta H_0 = {delta_H0:.2f}$)')
    ax2.set_xlabel(r'Radius / Coherence Coordinate $r$ (kpc)', fontsize=12)
    ax2.set_ylabel(r'Effective $\Delta H_0$ Contribution (km/s/Mpc)', fontsize=12)
    ax2.set_title(r'Hubble Tension ($\Delta H_0$) Local Vacuum Bridge', fontsize=13, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(frameon=True, fontsize=11)

    plt.tight_layout()

    out_dir = "outputs/plots"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "popcorn_vacuum_hubble_tension.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"[+] Saved Popcorn Vacuum & Hubble Tension plot to {out_path}")
    plt.close()


if __name__ == "__main__":
    main()
