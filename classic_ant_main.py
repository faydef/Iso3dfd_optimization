from representation import initiate
from update import update
from exec_algo import command,execute
import numpy as np
from random import choices
from operator import itemgetter
import sys
import time

def ant(nb_ant, nb_iteration, problem, rho, alpha, Q, timeout):
    liste, dico = initiate(problem)
    best = [[],0]
    for j in range(nb_iteration):
        #initiate the problem
        ants = [[],[],[]]
        time = []
        for i in range(nb_ant):
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
                start_time = time()
                ants[2].append(execute(command({'filename': '../iso3dfd-st7/compiled/bin_'+path[0]+'_'+path[1]+'.exe', 'size1':str(problem[0]), 'size2': str(problem[1]), 'size3':str(problem[2]), 'num_thread':str(path[2]), 'dim1':str(path[3]), 'dim2': str(path[4]), 'dim3': str(path[5])}), timeout))
                end_time = time()
                time.append(end_time-start_time)
        timeout = 0
        sum = 0
        for i in range(len(time)):
            timeout += ants[1][i]*time[i]
        timeout = int(timeout/nb_ant) + 1
        print(ants[2])
        print(timeout)
        #update the weight
        ants[0], ants[1], ants[2] = map(list, zip(*sorted(zip(ants[0], ants[1], ants[2]),key=itemgetter(2), reverse=True)))
        #update(routes= zip(ants[0][10], ants[1][10]), liste, dico, rho, alpha, Q)
        routes = [(ants[0][i], ants[1][i]) for i in range(min(10, len(ants[0])))]
        if ants[2][0] > best[1]:
            best = [ants[0][0], ants[2][0]]
        update(routes, liste, dico, rho, alpha, Q)
    return best

if __name__ == '__main__':
    _,nb_ant, nb_iteration, problem_1, problem_2, problem_3, rho, alpha, Q, timeout = sys.argv
    print(ant(int(nb_ant), int(nb_iteration), [int(problem_1), int(problem_2), int(problem_3)], float(rho), float(alpha), float(Q), int(timeout)))
        
        
        
        