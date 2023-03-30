from classic_ant_main import ant
import os
import sys
from operator import itemgetter

if __name__ == '__main__':
    _,nb_ant, nb_iteration, problem_1, problem_2, problem_3, timeout = sys.argv
    alpha_list = [0.25, 0.5, 0.75, 1, 1.25, 1.5,1.75]
    rho_list = [0.2, 0.4, 0.6, 0.8]
    Q_list = [0.25, 0.5, 0.75, 1]
    result = [[],[],[]]
    i = 1
    filename = 'results.txt'
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as f:
        for alpha in alpha_list:
            for rho in rho_list:
                for Q in Q_list:
                    print('step '+str(i)+'/112')
                    L = ant(int(nb_ant), int(nb_iteration), [int(problem_1), int(problem_2), int(problem_3)], rho, alpha, Q, int(timeout))
                    result[0].append((rho, alpha, Q))
                    result[1].append(L[0])
                    result[2].append(L[1])
                    f.write(str([(rho, alpha, Q), L[0], L[1]]) + '\n')
                    f.flush()  # flush the buffer to ensure data is written to file
                    i+=1
    result[0], result[1], result[2] = map(list, zip(*sorted(zip(result[0], result[1], result[2]),key=itemgetter(2), reverse=True)))
    print([(result[0][i], result[1][i], result[2][i]) for i in range(10)])
