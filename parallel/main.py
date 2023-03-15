import os
import sys
sys.path.append("..")



nb_machines = 4 

if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) == 1 :
        nb_ant = 10
        nb_iteration = 10
        problem_1 = 256
        problem_2 = 256
        problem_3 = 256
        rho = 0.6
        alpha = 0.25
        Q = 1
        timeout = 60
    else :
        (
            _,
            nb_ant,
            nb_iteration,
            problem_1,
            problem_2,
            problem_3,
            rho,
            alpha,
            Q,
            timeout,
        )= sys.argv
   
    content = "#!/bin/sh\nmpirun -np {} -map-by ppr:1:node:PE=1 -rank-by node python3 parallel.py".format(nb_machines)
 
    with open("script.sh","w") as f :
        f.write(content)
    os.system("sbatch -N 4 -n 128 --exclusive --qos=16nodespu --reservation=st76i6 script.sh")
    
    """
    print(
        ant(
            int(nb_ant),
            int(nb_iteration),
            [int(problem_1), int(problem_2), int(problem_3)],
            float(rho),
            float(alpha),
            float(Q),
            int(timeout),
        )
    )
    """

