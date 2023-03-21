#!/bin/bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/oneapi/compiler/2022.0.2/linux/compiler/lib/intel64_lin
if ls | grep "^slurm" >/dev/null; then
	rm slurm*
fi
sbatch -N 1  --qos=16nodespu -p PSO.sh