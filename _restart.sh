#!/bin/bash

for n in 800  #0 60 260 500 800
do
    cd n${n}
    sed "s/NNNN/${n}/g" ../run_restart.sh > ./run_restart.sh
    qsub run_restart.sh
    cd ../
done
