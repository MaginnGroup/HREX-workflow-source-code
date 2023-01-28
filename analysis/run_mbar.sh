#!/bin/bash
#$ -N bp-32_mbar
#$ -pe smp 2
#$ -r n
#$ -m ae
#$ -q hpc@@maginn
#$ -M nwang2@nd.edu

# This is a conda environment with alchemical_analysis
# installed
module load conda
conda activate py27

mkdir mbar
cd mbar

for nmol in n0 n60 n260 n500 n800
do
    mkdir ${nmol}/
    cd ${nmol}/

    # Copy the prd.xvg files which contain the delta_energies between
    # different lambda-windows to a single location
    for i in {0..23}; do
        cp ../../../${nmol}/$i/prd.xvg ./$i.xvg
    done
    # Run alchemical analysis. Use alchemical_analysis -h to see the options
    alchemical_analysis -f 10 -g -w -p "" > mbar.log
    cd ../
done

cd ../
