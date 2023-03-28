#!/bin/bash

echo "La chaîne passée en argument est : $@"


if [[ "$@" == *"--parallel"* ]]; then
	echo "Execution of ACO in parallel"
	sbatch run_parallel.sh
else
	srun -N 1 -n 32 --exclusive -p cpu_tp --pty python3 main.py $@
	echo "non parallèle"
fi


