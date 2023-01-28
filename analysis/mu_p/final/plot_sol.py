import unyt as u
import numpy as np
import pandas as pd
import seaborn as sea
import matplotlib
import matplotlib.pyplot as plt

from matplotlib.ticker import MultipleLocator, AutoMinorLocator

matplotlib.rc("font", family="sans-serif")
matplotlib.rc("font", serif="Arial")


def main():

    exp_path = "./press_conc_expt.txt"
    mu_liq_path = "./mu_liq.txt"
    mu_vap_path = "./HFC32_muV_298K.csv"
    df_vap = pd.read_csv(mu_vap_path, index_col=0)
    df_liq = pd.read_csv(
        mu_liq_path,
        sep="\s+",
        names=["x", "mu_ex","mu_ex_unc","mu_kJmol","mu_unc"],
        skiprows=1
    )
    df_exp = pd.read_csv(
        exp_path,
        sep="\s+",
        names=["P_bar", "x"],
        skiprows=1
    )

    liq_xs = df_liq["x"]
    liq_mus = df_liq["mu_kJmol"]
    vap_ps = df_vap["P_MPa"]
    vap_mus_pr = df_vap["mu_PR_kJmol"]
    vap_mus_vdw = df_vap["mu_VDW_kJmol"]

    ps_pr = np.interp(liq_mus, vap_mus_pr, vap_ps)
    ps_vdw = np.interp(liq_mus, vap_mus_vdw, vap_ps)

    fig, ax = plt.subplots()
    ax.plot(
        liq_xs,
        ps_pr,
        '--o',
        alpha=0.4,
        markersize=10,
        linewidth=2,
        label=r"REFPROP"
    )
    ax.plot(
        liq_xs,
        ps_vdw,
        '--o',
        alpha=0.4,
        markersize=10,
        linewidth=3,
        label=r"van der Waals"
    )
    format_fig(fig, ax)
    fig.savefig("p_vs_x_vdWvRPRP.pdf")

    fig, ax = plt.subplots()
    ax.plot(
        df_exp["x"],
        df_exp["P_bar"] / 10.0,
        '--s',
        c="black",
        alpha=0.6,
        markersize=8,
        linewidth=3,
        label=r"Experiment"
    )
    ax.plot(
        liq_xs,
        ps_pr,
        '--o',
        alpha=0.6,
        markersize=10,
        linewidth=3,
        label=r"Simulation"
    )
    format_fig(fig, ax)
    fig.savefig("p_vs_x.pdf")

    with open("results_final.txt", "w") as f:
        f.write("#x_molfraction, P_MPa\n")
        for x, p in zip(liq_xs, ps_pr):
            f.write(f"{x:8.3f} {p:8.3f}\n")


def format_fig(fig, ax):

    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.25)
    ax.set_xlabel(r"$x_\mathrm{R32}$", fontsize=26, labelpad=15)
    ax.set_ylabel(r"P (MPa)", fontsize=26, labelpad=15)
    ax.tick_params("both", direction="in", which="both", length=3, labelsize=20)
    ax.tick_params("both", which="major", length=6)
    ax.yaxis.set_ticks_position("both")
    ax.xaxis.set_ticks_position("both")
    ax.xaxis.set_major_locator(MultipleLocator(0.2))
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.legend(fontsize=20)
    plt.subplots_adjust(bottom=0.2, top=0.9, left=0.2, right=0.9)


if __name__ == "__main__":
    main()

