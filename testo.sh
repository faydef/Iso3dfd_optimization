#!/bin/bash
../iso3dfd-st7/compiled/bin_O2_avx2.exe 512 512 512 28 100 512 8 32 > yenamarre.txt
/opt/cpu_monitor/cpu_monitor.x --csv --quiet --redirect -- ./bin/iso3dfd_dev07_cpu_avx512_ft_nohbm.exe 80 1916 1146 128 600 80 14 80