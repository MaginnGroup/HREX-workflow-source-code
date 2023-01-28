#!/bin/bash
#$ -N bp-32-nNNNN
#$ -pe mpi-48 192
#$ -r n
#$ -m ae
#$ -q hpc
#$ -M nwang2@nd.edu

# Load modules; specific to GMX version compiled by RSD
# this version must be used on the HPC nodes (hpc queue)
module load mvapich2/2.3.1/intel/19.0
module load gcc/10.2.0

# This line makes GROMACS (gmx_mpi) appear on your PATH
# Be aware that the modules loaded above must be consistent
# with what was used for compilation
source /afs/crc.nd.edu/group/maginn/group_members/Ryan_DeFever/software/gromacs-2020_hpc/bin/GMXRC

# Unset OMP_NUM_THREADS environment variable to prevent
# conflict between -ntomp command line option for gmx mdrun
# and the value in the environment variable
unset OMP_NUM_THREADS

# Finally run everything
# This is a 192 core launch configuration (1 OMP thread/MPI thread)
# -multidir tells gmx to look for prd.tpr in each directory 0--23
# -nex is the number of attempted exchanges for each swap
# -replex says to attempt exchanges every 2000 steps
mpirun -np 192 gmx_mpi mdrun -v -deffnm prd -multidir 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 -nex 10000 -replex 2000
