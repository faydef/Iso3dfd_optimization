from representation import initiate
from update import update
from exec_algo import command, execute
import numpy as np
from random import choices
from operator import itemgetter
import sys
import time

# import os


def ant(nb_ant, nb_iteration, problem, rho, alpha, Q, timeout):
    """
    this function is the main function of the ant colony algorithm.
    parameters:
        nb_ant: number of ants
        nb_iteration: number of iterations
        problem: list of the dimensions of the problem
        rho: pheromone evaporation rate
        alpha: pheromone importance
        Q: pheromone deposit factor
        timeout: time limit for the command line execution
    return:
        best: best solution found
    """
    ##########################################initiate the problem###########################################
    liste, dico = initiate(problem)  # list of choices and there probability
    best = [[], 0]  # store the best solution with its Gflops
    worst = set()  # set of worst path to avoid them
    for j in range(nb_iteration):
        ##########################################initiate the ants###########################################
        ants = [
            [],
            [],
            [],
        ]  # liste of paths, number of ants that choosed this path and their score
        timer = []  # liste of execution time in order to update the timeout
        for i in range(nb_ant):
            ######################################choose randomly a path to explore based on probability weights##############################
            safe_path = True
            while safe_path:
                choices_1 = choices(liste["liste1"], weights=dico["mat1"], k=1)[0]
                choices_2 = choices(
                    liste["liste2"],
                    weights=dico["mat2"][liste["liste1"].index(choices_1)],
                    k=1,
                )[0]
                choices_3 = choices(
                    liste["liste3"],
                    weights=dico["mat3"][liste["liste2"].index(choices_2)],
                    k=1,
                )[0]
                choices_4 = choices(
                    liste["liste4"],
                    weights=dico["mat4"][liste["liste3"].index(choices_3)],
                    k=1,
                )[0]
                choices_5 = choices(
                    liste["liste5"],
                    weights=dico["mat5"][liste["liste4"].index(choices_4)],
                    k=1,
                )[0]
                choices_6 = choices(
                    liste["liste6"],
                    weights=dico["mat6"][liste["liste5"].index(choices_5)],
                    k=1,
                )[0]
                path = [
                    choices_1,
                    choices_2,
                    choices_3,
                    choices_4,
                    choices_5,
                    choices_6,
                ]
                if not (tuple(path) in worst):
                    safe_path = False
            ##########################################execute and store the path###########################################
            # if the path is already explored we increment the number of ants
            if path in ants[0]:
                ants[1][ants[0].index(path)] += 1
            # else we add the path to the list of paths and we excute the command line and store its Gflops and time execution
            else:
                ants[0].append(path)
                ants[1].append(1)
                start_time = time.time()
                ants[2].append(
                    execute(
                        command(
                            {
                                "filename": "../iso3dfd-st7/compiled/bin_"
                                + path[0]
                                + "_"
                                + path[1]
                                + ".exe",
                                "size1": str(problem[0]),
                                "size2": str(problem[1]),
                                "size3": str(problem[2]),
                                "num_thread": str(path[2]),
                                "dim1": str(path[3]),
                                "dim2": str(path[4]),
                                "dim3": str(path[5]),
                            }
                        ),
                        timeout,
                    )[0]
                )
                end_time = time.time()
                timer.append(end_time - start_time)
        # update the timeout
        timeout = 0
        for i in range(len(timer)):
            timeout += ants[1][i] * timer[i]
        timeout = int(timeout / nb_ant) + 1
        print(ants[2])
        print(timeout)
        # update the probability weight for the best 10 solution
        ants[0], ants[1], ants[2] = map(
            list,
            zip(
                *sorted(zip(ants[0], ants[1], ants[2]), key=itemgetter(2), reverse=True)
            ),
        )
        routes = [
            (ants[0][i], ants[1][i], ants[2][i]) for i in range(min(10, len(ants[0])))
        ]
        update(routes, liste, dico, rho, alpha, Q)
        # store the worst path to avoid them
        if len(ants[0]) > 20:
            for i in range(len(ants[0]) - 1, len(ants[0]) - 10, -1):
                worst.add(tuple(ants[0][i]))
            for i in range(len(ants[0]) - 10, 0, -1):
                if ants[2][i] == -99:
                    worst.add(tuple(ants[0][i]))
        # update the best solution
        if ants[2][0] > best[1]:
            best = [ants[0][0], ants[2][0]]
    return best


if __name__ == "__main__":
    (
        _,
        nb_ant, #default 16 
        nb_iteration, #default 10
        problem_1, #default 256
        problem_2, #default 256
        problem_3, #default 256
        rho, #default 0.6
        alpha, #default 0.25
        Q, #default 1
        timeout, #default 60
    ) = sys.argv
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
