#!/bin/bash
#$ -N bp-32-nNNNN
#$ -pe mpi-48 192
#$ -r n
#$ -m ae
#$ -q hpc
#$ -M nwang2@nd.edu

module load mvapich2/2.3.1/intel/19.0
module load gcc/10.2.0

# This line makes GROMACS (gmx_mpi) appear on your PATH
# Be aware that the modules loaded above must be consistent
# with what was used for compilation
source /afs/crc.nd.edu/group/maginn/group_members/Ryan_DeFever/software/gromacs-2020_hpc/bin/GMXRC
unset OMP_NUM_THREADS

# Then create dirs for all systems
for ((i=0;i<24;i++)); do
    cd $i
    gmx_mpi convert-tpr -s prd.tpr -extend 1000 -o prd.tpr # 20000 in ps
    cd ../
done

mpirun -np 192 gmx_mpi mdrun -v -deffnm prd -multidir 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 -nex 10000 -replex 2000 -cpi prd.cpt
