import unyt as u
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn


matplotlib.rc("font", family="sans-serif")
matplotlib.rc("font", serif="Arial")

R = 8.314 * u.Unit("J/(mol * K)")


def main():

    # For R32
    mass = 52.024 * u.amu
    Tc = 351.5 * u.K
    Pc = 5.816 * u.MPa
    Vc = 0.1210547 / 1000 * u.m**3 / u.mol

    T = 298.15 * u.K
    debroglie = compute_debroglie(mass, T)

    # Read values for PR EOS
    df_pr = pd.read_csv(
        "HFC32_PR_fugV_298.csv",
        skiprows=5,
        names=["T_K", "P_MPa", "phi"]
    )

    # Compute mu(P) for VdW EOS
    pressures = df_pr["P_MPa"].values * u.MPa
    phis = []
    for P in pressures:
        phi = calc_phi_vdw(T, P, Tc, Pc, Vc) 
        phis.append(phi)
    vdw_phis = np.array(phis)

    p_0 = 0.0001 * u.MPa
    mu_0 = mu_ideal_gas(T, p_0, debroglie)
    vdw_mus = mu_0 + R*T*np.log(vdw_phis) + R*T*np.log(pressures/p_0)
   
    # Read values for PR EOS
    df_pr = pd.read_csv(
        "HFC32_PR_fugV_298.csv",
        skiprows=5,
        names=["T_K", "P_MPa", "phi"]
    )
    pr_mus = mu_0 + R*T*np.log(df_pr["phi"].values) + R*T*np.log(df_pr["P_MPa"].values * u.MPa / p_0)

    df = df_pr.drop(columns=["phi"])
    df["mu_PR_kJmol"] = pr_mus.to_value("kJ/mol")
    df["mu_VDW_kJmol"] = vdw_mus.to_value("kJ/mol")

    df.to_csv("HFC32_muV_298K.csv")

    seaborn.set_palette("deep")

    fig, ax = plt.subplots()
    ax.plot(
        vdw_mus[::4,].to(u.kJ/u.mol),
        pressures[::4].to(u.MPa),
        '-o',
        alpha=0.4,
        markersize=4,
        linewidth=4,
        label=r"$\mu^{vap}_{vdW}$"
    )
    ax.plot(
        pr_mus[::4].to(u.kJ/u.mol),
        pressures[::4].to(u.MPa),
        '-o',
        alpha=0.4,
        markersize=4,
        linewidth=4,
        label=r"$\mu^{vap}_{PR}$"
    )


    #ax.set_ylim(-0.02, 1.02)
    #ax.set_xlim(-48, -34)
    ax.set_ylabel("P (MPa)", fontsize=26, labelpad=15)
    ax.set_xlabel(r"$\mu$ (kJ/mol)", fontsize=26, labelpad=15)
    ax.tick_params("both", direction="in", which="both", length=3, labelsize=20)
    ax.tick_params("both", which="major", length=6)
    ax.yaxis.set_ticks_position("both")
    ax.xaxis.set_ticks_position("both")
    #ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    ax.xaxis.set_major_locator(MultipleLocator(3))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.set_yscale("log")
    ax.legend(fontsize=20)

    fig.tight_layout()
    fig.savefig("mu-vap-R32.pdf")

    ax.set_yscale("linear")
    ax.set_ylim(0.58, 1.52)
    ax.set_xlim(-36.1, -34.4)
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.xaxis.set_minor_locator(MultipleLocator(0.25))
    ax.yaxis.set_major_locator(MultipleLocator(0.1))
    ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    plt.subplots_adjust(right=0.7)
    ax.grid(which="both", axis="y",alpha=0.6)
    ax.get_legend().remove()

    fig.savefig("mu-vap-R32_inset.pdf")


def compute_debroglie(mass, temperature):
    """Compute the thermal de Broglie wavelength

    Parameters
    ----------
    mass : u.unyt_quantity
       mass of the molecule
    temperature : u.unyt_quantity
       temperature

    Returns
    -------
    debroglie : u.unyt_quantity
    """
    return np.sqrt(2 * np.pi * u.hbar**2 / (mass * u.kb * temperature))

def mu_ideal_gas(temperature, pressure, debroglie):
    """Compute the ideal gas chemical potential in the thermodynamic limit

    Parameters
    ----------
    temperature : u.unyt_quantity
       temperature
    pressure : u.unyt_quantity
       pressure
    debroglie : u.unyt_quantity
        thermal de Broglie wavelength

    Returns
    -------
    mu : u.unyt_quantity
    """
    mu = - np.log(u.kb * temperature / (debroglie**3 * pressure))
    return mu * u.kb * temperature

def calc_phi_vdw(T, P, Tc, Pc, Vc):
    """Compute the fugacity coefficient with the van der Waals EOS

    Equation from: doi:10.1021/ed065p772

    Parameters
    ----------
    T : u.unyt_quantity
        temperature
    P : u.unyt_quantity
        pressure
    Tc : u.unyt_quantity
        critical temperature
    Pc : u.unyt_quantity
        critical pressure
    Vc : u.unyt_quantity
        critical volume
   
    Returns
    -------
    phi : float
        fugacity coefficient
    """
    a = (27./64.) * R**2 * Tc**2 / Pc
    b = R * Tc / (8. * Pc)

    a1 = -(R*T/P + b).to_value("m**3/mol")
    a2 = (a/P).to_value("m**6/mol**2")
    a3 = -(a*b/P).to_value("m**9/mol**3")
    roots = np.roots([1, a1, a2, a3])
    real_roots = roots[np.isreal(roots)]
    assert len(real_roots) > 0
    Vm = np.max(np.real(roots)) * u.m**3 / u.mol
    
    ln_phi = b/(Vm-b) - 2.*a/(R*T*Vm) + np.log(R*T/(P*(Vm-b)))
    return np.exp(ln_phi)

def mu_ideal_solution(n_molecules, temperature, volume, debroglie):
    """Compute the ideal portion of the chemical potential of a
    molecule in solution

    Parameters
    ----------
    n_molecules : int
       number of molecules in solution
    temperature : u.unyt_quantity
       temperature
    volume : u.unyt_quantity
       average volume of the system
    debroglie : u.unyt_quantity
        thermal de Broglie wavelength

    Returns
    -------
    mu : u.unyt_quantity
    """
    mu = - np.log(volume / (debroglie**3 * (n_molecules+1)))
    return mu * u.kb * temperature

if __name__ == "__main__":
    main()
