# HREX-Scripts
 Example files for Gromacs and scripts of "Alchemical Free Energy and Hamiltonian Replica Exchange Molecular Dynamics to Compute Hydrofluorocarbon Isotherms in Imidazolium-Based Ionic Liquids" 
 Author: Ning Wang, Ryan S. DeFever, and Edward J. Maginn
 1. In templates/ folder, prepare mol.gro and mol.itp 
    Run "source build_systems.sh" to get conf_nxxxx.gro and topol_nxxxx.top
 2. In main folder, run "source _setup-eq.sh" to perform equilibration 
 3. Then, run "source _setup-prod.sh" to perform production 
    Run "source _restart.sh" in case you reach the wall clock limit and need to restart
 4. In analysis/ folder, install the alchemical_analysis tool first. 
    Then, run "qsub run_mbar.sh" to perform MBAR analysis
 5. "git clone https://github.com/rsdefever/block_average.git"
 6. "python compute_mu.py" to get chemical potential in liquid phase
 7. In mu_p/ folder, "python compute_mu_vap.py" to get chemical potential in vapor phase from REFPROP data HFC32_PR_fugV_298.csv
 8. In final/ foler, prepare HFC32_muV_298K.csv, mu_liq.txt, and press_conc_expt.txt (from experiments) and run "python plot_sol.py" to get final result.
 
