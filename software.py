#!/usr/bin/env python3

import argparse
import subprocess
import socket
import os
try:
    from firework_algo import firework
    np = 'yes'
except ImportError:
    np = None

def main():
    Defaultalpha = 0.8
    Defaultrho = 0.25
    DefaultQ = 0.001
    Defaultc1 = 3.0
    Defaultc2 = 3.0
    Defaultw = 0.5
    timeout = 40
    nb_ants = 10
    nb_particles = 10
    nb_iteration = 10

    parser = argparse.ArgumentParser(description='Script to execute a specified file with given parameters')
    parser.add_argument('--optimize', '-o', metavar='proportion', help='The importance of GFLOPS and energy in optimization: 0 for optimizing only energy, and 1 for optimizing only GFLOPS', dest='prop', default=1)
    parser.add_argument('-n1', metavar='n1', help='Set the n1 parameter; problem size X ', dest='n1_value')
    parser.add_argument('-n2', metavar='n2', help='Set the n2 parameter; problem size Y ', dest='n2_value')
    parser.add_argument('-n3', metavar='n3', help='Set the n3 parameter; problem size Z ', dest='n3_value')
    parser.add_argument('--method', metavar='FILE', help='choose the optimization method to execute the specified file', dest='file_to_execute')
    parser.add_argument('-N', metavar='N', help='Number of nodes to use in parallel', dest='N_value')

    args = parser.parse_args()

    if float(args.prop) < 1:
        if socket.gethostname() == 'john3':
            if args.file_to_execute == 'PSO_nrj':
                output = subprocess.check_output(['python3', "PSO_nrj.py", str(nb_particles), str(nb_iteration), args.n1_value, args.n2_value, args.n3_value, str(timeout), str(Defaultc1), str(Defaultc2), str(Defaultw),args.prop])
                output_string = output.decode('utf-8')
                output_lines = output_string.split('\n')
                solution_line = None
                fitness_line = None
                for line in output_lines:
                    if 'Solution:' in line:
                        solution_line = line
                    if 'Fitness value:' in line:
                        fitness_line = line
        
                solution_str = solution_line.split(':')[1].strip()
                solution = list(map(str, solution_str[1:-1].split(',')))
                fitness_str = fitness_line.split(':')[1].strip()
                fitness = float(fitness_str)
                print(f"Fitness value: {fitness}")
                print(f"Solution: {solution}")
            if args.file_to_execute == 'ACO_nrj':
                subprocess.run(['python3', "ACO_nrj.py", str(nb_ants), str(nb_iteration), args.n1_value, args.n2_value, args.n3_value, str(timeout), str(Defaultc1), str(Defaultc2), str(Defaultw),args.prop])
    elif float(args.prop) == 1:
        if args.file_to_execute == 'ACO_par':
            filename = "my_script.sh"
            if os.path.exists(filename):
                os.remove(filename)
            with open("my_script.sh", "w") as f:
                # Write the contents of the file
                f.write("#!/bin/bash\n")
                f.write("#SBATCH --time=12:00:00\n")
                f.write(f"#SBATCH -N {int(args.N_value)}\n")
                f.write(f"#SBATCH -n {int(args.N_value)*32}\n")
                f.write("#SBATCH -p cpu_prod\n")
                f.write("#SBATCH --exclusive\n")
                f.write("#SBATCH --qos=16nodespu\n\n")
                f.write("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/oneapi/compiler/2022.0.2/linux/compiler/lib/intel64_lin\n\n")
                f.write("./generate_hostfile.sh\n")
                f.write("mpirun --hostfile hostfile --rank-by node --map-by ppr:1:node:PE=16 python3 parallel_ant_main.py "+str(nb_ants)+" "+str(nb_iteration)+" "+args.n1_value+" "+args.n2_value+" "+args.n3_value+" "+str(Defaultrho)+" "+str(Defaultalpha)+" "+ str(DefaultQ)+" "+ str(timeout)+"\n")
            subprocess.run(["chmod +x ./my_script.sh"], shell=True)
            subprocess.run(["sbatch ./my_script.sh"], shell=True)
        if args.file_to_execute == 'ACO':
            #print(f"Executing {""} with -n {args.n_value} and -p {args.I_value}")
            #subprocess.run(["python3", "classic_ant_main.py {} {} {} {} {} {} {} {} {}".format(args.A_value, args.I_value, args.n1_value, args.n2_value, args.n3_value, Defaultrho, Defaultalpha, DefaultQ, args.T_value)])
            subprocess.run(['python3', "classic_ant_main.py", str(nb_ants), str(nb_iteration), args.n1_value, args.n2_value, args.n3_value, str(Defaultrho), str(Defaultalpha), str(DefaultQ), str(timeout)])
        if args.file_to_execute == 'PSO':
            subprocess.run(['python3', "PSO.py", str(nb_particles), str(nb_iteration), args.n1_value, args.n2_value, args.n3_value, str(timeout), str(Defaultc1), str(Defaultc2), str(Defaultw)])
        if args.file_to_execute == 'fireworks':
            if np is None:
                    pass
            else:
                res = firework(10, 5, 5, "euclide", 0.8,1, 1, [int(args.n1_value), int(args.n2_value), int(args.n3_value)],timeout)
                print(res)


if __name__ == '__main__':
    main()
