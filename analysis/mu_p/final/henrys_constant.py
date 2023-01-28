#Henry's constant calculation @ Ning Wang
import unyt as u
import numpy as np
import panedr
import pandas as pd

def main():

    # Compute the thermal debroglie wavelength
    temperature = 298.15 * u.K
    pressure = 1.0 * u.bar
    mass = 52.024 * u.amu  # For HFC-32

    mu_liq_path = "./mu_liq.txt"
    df_liq = pd.read_csv(
        mu_liq_path,
        sep="\s+",
        names=["x", "mu_ex","mu_ex_unc","mu_kJmol","mu_unc"],
        skiprows=1
    )
    liq_mus = df_liq["mu_ex"]
    mu_ex= liq_mus[0]*u.kJ/u.mol
    
    edr_path = f"../../../n0/0/prd.edr"
    df = panedr.edr_to_df(edr_path)
    # Calculate the average volume
    avg_vol = df["Volume"].mean() * u.nm**3

    k = henrys_constant(temperature,avg_vol,mu_ex)

    print(k.to_value('MPa'))

def henrys_constant(temperature, vol, mu):
    
    return u.kb * temperature * 400/vol * np.exp(mu/(u.kb * temperature))

if __name__ == "__main__":
    main()
