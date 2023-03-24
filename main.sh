#!/bin/sh
#SBATCH --time=12:00:00
#SBATCH -N 4
#SBATCH -n 128
#SBATCH -p cpu_prod
#SBATCH --exclusive
#SBATCH --qos=16nodespu
#SBATCH --sockets-per-node=2
#SBATCH --cores-per-socket=8

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/oneapi/compiler/2022.0.2/linux/compiler/lib/intel64_lin

cd intel_ant_colony
# Use the script to generate the hostfile
./generate_hostfile.sh

mpirun --hostfile hostfile --rank-by node --map-by ppr:1:node:PE=32 python3 parallel_ant_main.py 32 10 128 128 128 0.8 0.25 1 30
