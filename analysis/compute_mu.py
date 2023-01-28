# Import statements;
# unyt, numpy, and panedr are available from conda
# block_average is a custom package
# (github.com/rsdefever/block_average)
import unyt as u
import numpy as np
import panedr
from block_average import estimate_variance


def main():

    # Compute the thermal debroglie wavelength
    temperature = 298.15 * u.K
    pressure = 1.0 * u.bar
    mass = 52.024 * u.amu  # For HFC-32
    debroglie = compute_debroglie(mass, temperature)

    # Order of mus_ex_soln and mus_ex_unc must
    # match n_mols
    n_mols = np.array([0, 60, 260,500,800])
    # Note the sign flip; MBAR computed the
    # free energy of removing a molecule
    mus_ex_soln = [
        -6.192,
        -6.235,
        -6.605,
        -6.947,
        -7.199
    ] * u.kJ/u.mol

    mus_ex_unc = [
        0.027,
        0.025,
        0.022,
        0.020,
        0.019
    ] * u.kJ/u.mol

    # Calculate the mol fraction for each system
    concs = [nmol/(400+nmol) for nmol in n_mols]
    # Lists to store average volume and ideal chemical potential
    volumes = []
    mus_id_unc = []
    for nmol in n_mols:
        # Use the volume from the non-interacting system
        # which is replica 23
        # edr file stores all thermodynamic output in binary form
        edr_path = f"../n{nmol}/23/prd.edr"
        df = panedr.edr_to_df(edr_path)
        # Calculate the average volume
        avg_vol = df["Volume"].mean()
        # Compute hte variance
        var_est, var_err = estimate_variance(df["Volume"].values)
        # Propogate the uncertainty in the volume to the chemical potential
        unc = np.sqrt((u.kb * temperature / (avg_vol * u.nm**3))**2 * var_est * u.nm**6)
        # Save the volume and uncertainty
        mus_id_unc.append(unc.to_value(u.kJ/u.mol))
        volumes.append(avg_vol)

    # Add units to volume and mu_id_unc
    vols = np.asarray(volumes) * u.nm**3
    mus_id_unc = np.asarray(mus_id_unc) * u.kJ/u.mol

    # Compute mu_ideal for each system
    mus_ideal_soln = mu_ideal_solution(n_mols, temperature, vols, debroglie)

    # Compute total chemical potential for each system
    mus_soln = mus_ideal_soln + mus_ex_soln
    mus_unc = mus_ex_unc + mus_id_unc

    # Save results to file
    with open("mu_liq.txt", "w") as fout:
        fout.write("# x_HFC, mu_ex, mu_ex_unc, mu, mu_unc\n")
        for x, mu_ex, mu_ex_unc, mu, mu_unc in zip(concs, mus_ex_soln, mus_ex_unc, mus_soln, mus_unc):
            mu_ex = mu_ex.to_value(u.kJ/u.mol)
            mu_ex_unc = mu_ex_unc.to_value(u.kJ/u.mol)
            mu = mu.to_value(u.kJ/u.mol)
            mu_unc = mu_unc.to_value(u.kJ/u.mol)
            fout.write(
                    f"{x:8.3f}{mu_ex:10.3f}{mu_ex_unc:10.3f}"
                    f"{mu:10.3f}{mu_unc:10.3f}\n"
            )



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
