from representation import initiate
from update import update
from exec_algo import command,execute
import numpy as np
from random import choices
from operator import itemgetter
import sys
import time
import os

def ant(nb_ant, nb_iteration, problem, rho, alpha, Q, timeout):
    liste, dico = initiate(problem)
    best = [[],0]
    worst = []
    for j in range(nb_iteration):
        #initiate the problem
        ants = [[],[],[]]
        timer = []
        for i in range(nb_ant):
            choices_1 = choices(liste['liste1'], weights=dico['mat1'], k=1)[0]
            choices_2 = choices(liste['liste2'], weights=dico['mat2'][liste['liste1'].index(choices_1)], k=1)[0]
            choices_3 = choices(liste['liste3'], weights=dico['mat3'][liste['liste2'].index(choices_2)], k=1)[0]
            choices_4 = choices(liste['liste4'], weights=dico['mat4'][liste['liste3'].index(choices_3)], k=1)[0]
            choices_5 = choices(liste['liste5'], weights=dico['mat5'][liste['liste4'].index(choices_4)], k=1)[0]
            choices_6 = choices(liste['liste6'], weights=dico['mat6'][liste['liste5'].index(choices_5)], k=1)[0]
            path = [choices_1, choices_2, choices_3, choices_4, choices_5, choices_6]
            while path in worst:
                choices_1 = choices(liste['liste1'], weights=dico['mat1'], k=1)[0]
                choices_2 = choices(liste['liste2'], weights=dico['mat2'][liste['liste1'].index(choices_1)], k=1)[0]
                choices_3 = choices(liste['liste3'], weights=dico['mat3'][liste['liste2'].index(choices_2)], k=1)[0]
                choices_4 = choices(liste['liste4'], weights=dico['mat4'][liste['liste3'].index(choices_3)], k=1)[0]
                choices_5 = choices(liste['liste5'], weights=dico['mat5'][liste['liste4'].index(choices_4)], k=1)[0]
                choices_6 = choices(liste['liste6'], weights=dico['mat6'][liste['liste5'].index(choices_5)], k=1)[0]
                path = [choices_1, choices_2, choices_3, choices_4, choices_5, choices_6]
            if path in ants[0]:
                ants[1][ants[0].index(path)] += 1
            else:
                ants[0].append(path)
                ants[1].append(1)
                start_time = time.time()
                ants[2].append(execute(command({'filename': '../iso3dfd-st7/compiled/bin_'+path[0]+'_'+path[1]+'.exe', 'size1':str(problem[0]), 'size2': str(problem[1]), 'size3':str(problem[2]), 'num_thread':str(path[2]), 'dim1':str(path[3]), 'dim2': str(path[4]), 'dim3': str(path[5])}), timeout))
                end_time = time.time()
                timer.append(end_time-start_time)
        timeout = 0
        for i in range(len(timer)):
            timeout += ants[1][i]*timer[i]
        timeout = int(timeout/nb_ant) + 1
        print(ants[2])
        print(timeout)
        #update the weight
        ants[0], ants[1], ants[2] = map(list, zip(*sorted(zip(ants[0], ants[1], ants[2]),key=itemgetter(2), reverse=True)))
        routes = [(ants[0][i], ants[1][i]) for i in range(min(10, len(ants[0])))]
        if len(ants[0]) > 10:
            worst = [ants[0][i] for i in range(len(ants[0])-1, max(-1, len(ants[0])-5),-1)]
        if ants[2][0] > best[1]:
            best = [ants[0][0], ants[2][0]]
        update(routes, liste, dico, rho, alpha, Q)
    return best

if __name__ == '__main__':
    _,nb_ant, nb_iteration, problem_1, problem_2, problem_3, no_rho, no_alpha, no_Q, timeout = sys.argv
    # alpha_list = [0.25, 0.5, 0.75, 1, 1.25, 1.5,1.75]
    # rho_list = [0.2, 0.4, 0.6, 0.8]
    # Q_list = [0.25, 0.5, 0.75, 1]
    # result = [[],[],[]]
    # i = 1
    # for alpha in alpha_list:
    #     for rho in rho_list:
    #         for Q in Q_list:
    #             print('step '+str(i)+'/112')
    #             L = ant(int(nb_ant), int(nb_iteration), [int(problem_1), int(problem_2), int(problem_3)], rho, alpha, Q, int(timeout))
    #             result[0].append((rho, alpha, Q))
    #             result[1].append(L[0])
    #             result[2].append(L[1])
    #             i+=1
    # result[0], result[1], result[2] = map(list, zip(*sorted(zip(result[0], result[1], result[2]),key=itemgetter(2), reverse=True)))
    # print([(result[0][i], result[1][i], result[2][i]) for i in range(10)])

    filename = 'results.txt'
    with open(filename, 'w') as f:
        for i in range(2):
            print('step '+str(i+1)+'/2')
            if os.path.exists(filename):
                os.remove(filename)
            L = ant(int(nb_ant), int(nb_iteration), [int(problem_1), int(problem_2), int(problem_3)], float(rho), float(alpha), float(Q), int(timeout))
            f.write(str(L) + '\n')
            f.flush()  # flush the buffer to ensure data is written to file
        
        
        