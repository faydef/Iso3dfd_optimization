#!/bin/bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/oneapi/compiler/2022.0.2/linux/compiler/lib/intel64_lin
cd ..
mpirun -np 4 -map-by ppr:1:node:PE=4 -rank-by node python3 parallel.py 32 20 256 256 256 0.6 0.25 1  
