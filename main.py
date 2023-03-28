from classic_ant_main import ant
from tree_ant_main import tree_ant
from PSO import objective_function, ParticleSwarmOptimization
from firework_algo import firework
import argparse
import numpy as np
import sys

compil_flag_list = ["O2", "O3", "Ofast"]
simd_list = ["avx", "avx2", "avx512"]
output_value = 'points'

DefaultIterMax = 10
DefaultMethod = "ACO"
Defaultnumberpopulation = 100
Defaultnfirework = 5
Defaultalpha = 0.8
Defaultrho = 0.25
DefaultQ = 1
Defaultc1 = 1.5
Defaultc2 = 1.5
Defaultw = 0.8
Defaultn1 = 256
Defaultn2 = 256
Defaultn3 = 256
Defaultnthread = 32
Defaulttimeout = 30
Defaulta = 0.04
Defaultb = 0.8
Defaultts = 50
Defaultamp = 60
Defaultngs = 5


def cmdLineParsing():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--i", help="maximum nb of iterations", default=DefaultIterMax, type=int)
    parser.add_argument(
        "--n1", help="problem size along first axis default:256", default=Defaultn1, type=int)
    parser.add_argument(
        "--n2", help="problem size along first axis default:256", default=Defaultn2, type=int)
    parser.add_argument(
        "--n3", help="problem size along first axis default:256", default=Defaultn3, type=int)
    parser.add_argument(
        "--nt", help="maximum number of thread default:32", default=Defaultnthread, type=int)
    parser.add_argument(
        "--m", help="population based method (ACO, Tree_ACO, PSO,firework) default:ACO", default=DefaultMethod)
    
    parser.add_argument(
        "--rho", help="evaporation_rate for ant colonies default:0.8", default=Defaultalpha, type=np.float64)
    parser.add_argument(
        "--alpha", help="value of exponent for ant colonies default:0.25", default=Defaultrho, type=np.float64)
    parser.add_argument(
        "--q", help="quantity if pheromons deposed for ant colonies default:1", default=DefaultQ, type=np.float64)
    parser.add_argument(
        "--c1", help="particle speed for PSO default:0.5", default=Defaultc1, type=np.float64)
    parser.add_argument(
        "--c2", help="group speed for PSO default:0.5", default=Defaultc2, type=np.float64)
    parser.add_argument(
        "--w", help="particle inertia for PSO default:", default=Defaultw, type=np.float64)
    parser.add_argument(
        "--t", help="duration before timeout default:30", default=Defaulttimeout, type=int)
    parser.add_argument(
        "--a", help="minimum rate sparks/firework", default=Defaulta, type=np.float64)
    parser.add_argument(
        "--b", help="maximum rate sparks/firework", default=Defaultb, type=np.float64)
    parser.add_argument(
        "--ts", help="ts : total number of sparks generated by n fireworks default:50", default=Defaultts, type=int)
    parser.add_argument(
        "--amp", help="maximum explosion amplitude default:60", default=Defaultamp, type=np.float64)
    parser.add_argument(
        "--ngs", help="ngs : total number of sparks generated by gaussian distribution default:5", default=Defaultngs, type=int)

    
    parser.add_argument(
        "--ts", help="number of particles/ants/fireworks on each iteration default:100 for population,5 for firework", default=Defaultnfirework, type=int)
    
    parser.add_argument(
        "--n", help="number of particles/ants/fireworks on each iteration default:100/5 for firework", default=Defaultnumberpopulation, type=int)
    
    args = parser.parse_args()

    if args.i <= 0:
        sys.exit(
            "Error: maximum nb of iterations must be an integer greater than 0!")

    if args.m not in ("ACO", "Tree_ACO", "PSO", "firework"):
        sys.exit(
            "Error: local method must be in: [ACO, Tree_ACO, PSO,firework]!")

    return args.i, args.n1, args.n2, args.n3, args.m, args.n, args.nt, args.alpha, args.rho, args.q, args.c1, args.c2, args.w,  args.t, args.a, args.b, args.ts, args.amp, args.ngs


def ask_for(question, default_value):
    res = input(question)
    if res == "":
        return default_value
    else:
        return int(res)


i, n1, n2, n3, method, n, n_threads_max, alpha, rho, Q, c1, c2, w,  timeout, a, b, totalspark, amplitude, gauss_sparks = cmdLineParsing()

if not len(sys.argv) > 1:
    type_algo = int(input(
        "Which algorithm would you want to execute ? classic ant colony (0) or tree ant colony (1) or particle swarm (2)? "))
    while type_algo not in [0, 1, 2]:
        print("please enter a valid algorithm")
        type_algo = int(input(
            "Which algorithm would you want to execute ? classic ant colony (0) or tree ant colony (1) or particle swarm (2)? "))

    if type_algo == 0 or type_algo == 1:
        nb_iter = ask_for(
            "number of iterations (10 by default) : ", DefaultIterMax)
        nb_ants = ask_for(
            "number of ants per iteration (100 by default) : ", Defaultnumberpopulation)
        evaporation_rate = input(
            "evaporation_rate (0.8 by default) : ") or Defaultalpha
        n1_size = ask_for(
            "size of the problem x (default size 256) : ", Defaultn1)
        n2_size = ask_for(
            "size of the problem y (default size 256) : ", Defaultn2)
        n3_size = ask_for(
            "size of the problem z (default size 256) : ", Defaultn3)
        n_threads_max = ask_for(
            "maximum number of threads (32 by default): ", 32)

    if type_algo == 0:
        print("executing classic ant colony optimization...")
        problem = [n1_size, n2_size, n3_size]
        ant(nb_ants, nb_iter, problem, rho,  evaporation_rate, Q, timeout)
    if type_algo == 1:
        print("executing ant colony optimization on a tree...")
        tree_ant(compil_flag_list, simd_list, n_threads_max, n1_size,
                 n2_size, n3_size, evaporation_rate, nb_iter, nb_ants)
    if type_algo == 2:
        max_iterations = ask_for("number of iterations (10 by default) : ", 10)
        num_particles = ask_for(
            "number of particles per iteration (100 by default) : ", 100)
        c1 = input("particle speed (1.5 by default) : ") or 1.5
        c2 = input("group_speed (1.5 by default) : ") or 1.5
        w = input("inertia (0.5 by default) : ") or Defaultw
        problem_1 = ask_for(
            "size of the problem x (default size 256) : ", Defaultn1)
        problem_2 = ask_for(
            "size of the problem y (default size 256) : ", Defaultn2)
        problem_3 = ask_for(
            "size of the problem z (default size 256) : ", Defaultn3)
        n_threads_max = ask_for(
            "maximum number of threads (32 by default) : ", 32)
        timeout = ask_for(
            "duration before timeout (30 by default) : ", 30)
        print("executing particle swarm optimization...")

        bounds = [(0, 2), (0, 2), (1, n_threads_max), (16, problem_1),
                  (1, problem_2), (1, problem_3)]
        optimizer = ParticleSwarmOptimization(
            objective_function,
            bounds,
            num_particles,
            max_iterations,
            c1,
            c2,
            w,
            [problem_1, problem_2, problem_3],
            timeout,
        )
        solution = optimizer.optimize()
        solution_parameters = []
        solution_parameters.append(compil_flag_list[solution[0][0]])
        solution_parameters.append(simd_list[solution[0][1]])
        solution_parameters.append(solution[0][2])
        solution_parameters.append(solution[0][3])
        solution_parameters.append(solution[0][4])
        print("Solution: ", solution_parameters)
        print("Fitness value: ", solution[1])

if len(sys.argv) > 1:
    if method == "ACO":
        problem = [n1, n2, n3]
        ant(n, i, problem, rho, alpha, Q, timeout)
    if method == "Tree_ACO":
        tree_ant(compil_flag_list, simd_list, n_threads_max, n1,
                 n2, n3, alpha, i, n, timeout)
    if method == "PSO":
        bounds = [(0, 2), (0, 2), (1, n_threads_max), (16, n1),
                  (1, n2), (1, n3)]
        optimizer = ParticleSwarmOptimization(
            objective_function,
            bounds,
            n,
            i,
            c1,
            c2,
            w,
            [n1, n2, n3],
            timeout,
        )
        solution = optimizer.optimize()
        solution_parameters = [compil_flag_list[solution[0][0]],
                               simd_list[solution[0][1]], solution[0][2], solution[0][3], solution[0][4]]
        print("Solution: ", solution_parameters)
        print("Fitness value: ", solution[1])
    if method == "firework":
        res = firework(n, a, b, "euclide", totalspark, gauss_sparks, amplitude)
        print(res)
