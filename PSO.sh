#!/bin/sh
#SBATCH --time=12:00:00
#SBATCH -N 1
#SBATCH -n 32
#SBATCH -p cpu_prod
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/oneapi/compiler/2022.0.2/linux/compiler/lib/intel64_lin
cd intel_ant_colony
python3 tuningPSO.py 100 20 512 512 512 30

