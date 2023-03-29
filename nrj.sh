#!/bin/bash
sshpass -p 'your_password' ssh root@second_machine 'sudo /opt/cpu_monitor/cpu_monitor.x --csv --quiet --redirect -- ./bin/iso3dfd_dev07_cpu_avx512_ft_nohbm.exe 80 1916 1146 128 600 80 14 80' > output.txt
sshpass -p 'your_password' scp root@second_machine:output.txt intel_ant_colony/output.txt
cat intel_ant_colony/output.txt

sshpass -p 'your_password' scp root@second_machine:output.txt intel_ant_colony/output.txt

sudo cp /home/USER1/FNAME /home/USER2/FNAME && sudo chown USER2:USER2 /home/USER2/FNAME