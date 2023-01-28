#!/bin/bash
#$ -N bp-32-nNNNN
#$ -pe smp 64
#$ -r n
#$ -m ae
#$ -q hpc@@maginn
#$ -M nwang2@nd.edu

module load mvapich2/2.3.1/intel/19.0
module load gcc/10.2.0
source /afs/crc.nd.edu/group/maginn/group_members/Ryan_DeFever/software/gromacs-2020_hpc/bin/GMXRC
unset OMP_NUM_THREADS

# First energy minimize and equilibrate
# Equilibration performed with R32 OFF!
mkdir em-eq/
cd em-eq/
cp ../templates/min.mdp .
cp ../templates/eql.mdp ./eql.mdp
cp ../templates/eql2.mdp ./eql2.mdp
gmx_mpi grompp -f min.mdp -c ../templates/conf.gro -p ../templates/topol.top -o min
mpirun -np 8 gmx_mpi mdrun -deffnm min -v -ntomp 8 -pinoffset 0 -pin on
gmx_mpi grompp -f eql.mdp -c min -p ../templates/topol.top -o eql
mpirun -np 8 gmx_mpi mdrun -deffnm eql -v -ntomp 8 -pinoffset 0 -pin on
gmx_mpi grompp -f eql2.mdp -c eql.gro -p ../templates/topol.top -o eql2
mpirun -np 8 gmx_mpi mdrun -deffnm eql2 -v -ntomp 8 -pinoffset 0 -pin on
cd ../

# Then create dirs for all systems
for ((i=0;i<24;i++)); do
    mkdir $i
    cd $i
    cp ../templates/min.mdp .
    gmx_mpi trjconv -s ../em-eq/eql2.tpr -f ../em-eq/eql2.xtc --dump $((10000-$i*100)) -o start.gro <<< "System"
    gmx_mpi grompp -f min.mdp -c start.gro -p ../templates/topol.top -o min
    mpirun -np 8 gmx_mpi mdrun -deffnm min -v -ntomp 8 -pinoffset 0 -pin on
    sed 's/MYLAMBDA/'$i'/g' ../templates/prd.mdp > prd.mdp
    gmx_mpi grompp -f prd.mdp -c min.gro -p ../templates/topol.top -o prd
    cd ../
done

