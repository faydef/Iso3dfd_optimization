from classic_ant_main import ant
import os
import sys
from operator import itemgetter

if __name__ == '__main__':
    _,nb_ant, nb_iteration, problem_1, problem_2, problem_3, timeout = sys.argv
    parameter_combinations = [
    (1.0, 0.1, 10),
    (1.0, 0.3, 10),
    (1.0, 0.5, 10),
    (1.0, 0.7, 10),
    (1.0, 0.9, 10),
    (2.0, 0.1, 10),
    (2.0, 0.3, 10),
    (2.0, 0.5, 10),
    (2.0, 0.7, 10),
    (2.0, 0.9, 10),
    (3.0, 0.1, 10),
    (3.0, 0.3, 10),
    (3.0, 0.5, 10),
    (3.0, 0.7, 10),
    (3.0, 0.9, 10),
    (1.0, 0.5, 50),
    (1.0, 0.5, 100),
    (1.0, 0.5, 200),
    (2.0, 0.5, 50),
    (2.0, 0.5, 100),
    (2.0, 0.5, 200),
    (3.0, 0.5, 50),
    (3.0, 0.5, 100),
    (3.0, 0.5, 200),
    ]


    result = [[],[],[]]
    i = 1
    filename = 'results_tuning_2.txt'
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as f:
        for elem in parameter_combinations:
            alpha,rho,Q = elem
            print('step '+str(i)+'/'+str(len(parameter_combinations)))
            L = ant(int(nb_ant), int(nb_iteration), [int(problem_1), int(problem_2), int(problem_3)], rho, alpha, Q, int(timeout))
            result[0].append((rho, alpha, Q))
            result[1].append(L[0])
            result[2].append(L[1])
            f.write(str([(rho, alpha, Q), L[0], L[1]]) + '\n')
            f.flush()  # flush the buffer to ensure data is written to file
            i+=1
    result[0], result[1], result[2] = map(list, zip(*sorted(zip(result[0], result[1], result[2]),key=itemgetter(2), reverse=True)))
    print([(result[0][i], result[1][i], result[2][i]) for i in range(10)])
