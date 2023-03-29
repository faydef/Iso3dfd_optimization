# coding:utf-8

from tree_graph_generation import *
from tree_graph_ant_colony import *
from tree_graph_tree_update import *
from exec_algo import *
from compile_all import *

output_value = "points"

# print(n_size)
# print(n_threads_max)


def tree_ant(
    compil_flag_list,
    simd_list,
    n_threads_max,
    n1_size,
    n2_size,
    n3_size,
    evaporation_rate,
    nb_iter,
    nb_ants,
    timeout,
):
    print("génération de l'arbre...")
    tree_graph, list_dict_parameters = tree_generation(
        compil_flag_list, simd_list, n_threads_max, n1_size, n2_size, n3_size
    )
    print("exécution de l'algo...")
    for i in range(nb_iter):
        print("generation number {}".format(i))
        ants_int = exploration(tree_graph, nb_ants)
        ants = [
            [list_dict_parameters[j][ants_int[k][j]] for j in range(len(ants_int[k]))]
            for k in range(nb_ants)
        ]
        # for k in range(nb_ants):
        #    ant_int_path = ants_int[k]
        #    ant_path = []
        #    for j in range(len(ant_int_path)):
        #        ant_path.append(list_dict_parameters[j][ant_int_path[j]])
        #    ants.append(ant_path)
        ants_score = []
        for ant in ants:
            olevel = ant[0]
            simd = ant[1]
            num_threads = str(ant[2])
            dim1 = str(ant[3])
            dim2 = str(ant[4])
            dim3 = str(ant[5])
            filename = "../iso3dfd-st7/compiled/bin_{}_{}.exe".format(olevel, simd)
            options = {
                "filename": filename,
                "size1": str(n1_size),
                "size2": str(n2_size),
                "size3": str(n3_size),
                "num_thread": str(num_threads),
                "dim1": str(dim1),
                "dim2": str(dim2),
                "dim3": str(dim3),
            }
            bash_command = command(options)
            score = execute(bash_command, timeout)
            if output_value == "flops":
                print(str(score) + " GFlops")
            elif output_value == "points":
                print(str(score) + " MPoints/s")
            ants_score.append(score)
        if i < nb_iter - 1:
            # sinon update_tree cleanerait les listes ants et ants_score
            update_tree(tree_graph, evaporation_rate, ants_int, ants_score)
        best_ant = BestAnt(ants)
    print(ants)
    print(ants_score)
    last_ants = list(zip(ants_score, ants))
    best_ant = max(BestAnt(last_ants), best_ant)
    if output_value == "flops":
        print("best score : {} GFlops".format(best_ant[0]))

    elif output_value == "points":
        print("best ant : {}".format(best_ant[1]))
    print("best score : {} MPoints/s".format(best_ant[0]))
