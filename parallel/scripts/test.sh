#!/bin/bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/oneapi/compiler/2022.0.2/linux/compiler/lib/intel64_lin
../../../iso3dfd-st7/compiled/bin_O1_avx2.exe 256 256 256 4 100 256 256 256 
echo "bonjour"
