#!/bin/bash

# Switch into each directory and submit the production simulations
# Equilibration step must have finished first, or this will fail
# Easy check: make sure inside n${n} that directories exist for
# each HREX lambda-window and that prd.tpr exists for each lambda-window

for n in 0 60 260 500 800
do
    cd n${n}
    sed "s/NNNN/${n}/g" ../run-hpc.sh > ./run-hpc.sh
    qsub run-hpc.sh
    cd ../
done
