#!/bin/bash

for n in 0 60 260 500 800
do
    mkdir n${n}
    cd n${n}
    # Make a template directory for n${n} specifically
    mkdir templates
    # Copy all mdp, itp files
    cp ../templates/*mdp templates/.
    cp ../templates/R32.itp templates/.
    # Copy the .gro and .top files corresponding to n=$n
    cp ../templates/conf_n${n}.gro templates/conf.gro
    cp ../templates/topol_n${n}.top templates/topol.top
    # Copy the run.sh and SGE submission scripts for the equilibration
    sed "s/NNNN/${n}/g" ../run-eq.sh > ./run-eq.sh
    # Submit the job to SGE scheduler
    qsub run-eq.sh
    cd ../
done
