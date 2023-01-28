#!/bin/bash

module load mpich/3.3/gcc
source /afs/crc.nd.edu/group/maginn/group_members/Ryan_DeFever/software/gromacs-2020.4/gromacs-mpi/bin/GMXRC

gmx_mpi insert-molecules -box 7.8 7.8 7.8 -nmol 400 -ci BMIM.gro -o tmp1.gro --try 20
gmx_mpi insert-molecules -f tmp1.gro -ci PF6.gro -o tmp2.gro -nmol 400 --try 20

for n in 0 60 260 500 800
do
    gmx_mpi insert-molecules -f tmp2.gro -ci R32.gro -o conf_n${n}.gro -nmol $(($n+1)) --try 50
    sed "s/NNNN/${n}/g" topol_template.top > topol_n${n}.top
done

rm -f tmp1.gro
rm -f tmp2.gro
