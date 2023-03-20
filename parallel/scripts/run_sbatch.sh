#!/bin/bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/oneapi/compiler/2022.0.2/linux/compiler/lib/intel64_lin
if ls | grep "^slurm" >/dev/null; then
	rm slurm*
fi
sbatch -N 4 -n 64 --exclusive --qos=16nodespu --reservation=st76intel7 -p cpu_prod run_parallel.sh
