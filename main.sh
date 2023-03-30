#!/bin/sh
#SBATCH --time=12:00:00
#SBATCH -N 16
#SBATCH -n 512
#SBATCH -p cpu_prod
#SBATCH --exclusive
#SBATCH --qos=16nodespu


export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/oneapi/compiler/2022.0.2/linux/compiler/lib/intel64_lin

#cd intel_ant_colony
# Use the script to generate the hostfile
./generate_hostfile.sh

/usr/bin/mpirun --hostfile hostfile --rank-by node --map-by ppr:1:node:PE=16 python3 parallel_ant_main.py $1 $2 $3 $4 $5 $6 $7 $8 30
#/usr/bin/mpirun --hostfile hostfile --rank-by node --map-by ppr:1:node:PE=16 python3 parallel_ant_main.py 100 40 512 512 512 0.8 0.25 0.0001 30 
