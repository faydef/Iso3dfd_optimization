#!/bin/bash
cd ..
mpirun -np 4 -map-by ppr:1:core:PE=1 python3 parallel.py 16 2 256 256 256 0.6 0.25 1  
