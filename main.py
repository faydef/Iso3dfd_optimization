#coding:utf-8

from tree_graph_generation import *
from tree_graph_ant_colony import *
from exec_algo import *


def ask_for(question,default_value):
    res = input(chaine)
    if res == "" :
        return default_value
    else :
        return int(res)


compil_flag_list = ["01","02","03","0fast"]
simd_list = ["sse","avx","avx2","avx512"]


type_algo = int(input("Which algorithm would you want to execute ? classic ant colony (0) or tree ant colony (1) ? "))



while type_algo not in [0,1]:
    print("please enter a valid algorithm")
if type_algo == 0 :
    print("execution of classic ant colony...")
    ###
if type_algo == 1: 
    print("exection of ant colony on a tree...") 


nb_iter = ask_for("number of iterations : ",10)
nb_ant = ask_for("number of ants per iteration : ",10)
evaporation_rate = ask_for("evaporation_rate",0)
n1_size = ask_for("size of the problem x : ",256)
n2_size = ask_for("size of the problem y : ",256)
n3_size = ask_for("size of the problem z : ",256)
n_threads_max = ask_for("maximum number of threads : ",32)


list_num_thread = values_num_thread_power_of_2(n_threads_max)


#print(n_size)
#print(n_threads_max)


if type_algo == 1 :
    tree_graph = tree_generation(compil_flag_list,simd_list,n_threads_max,n1_size,n2_size,n3_size)

    for _ in range(nb_iter):    
        ants = exploration(tree_graph,nb_ants)
        ants_score = []
        for ant in ants :
            options = {"filename" : filename, "size1":n1_size,"size2":n2_size,"size3":n3_size,\
                    "num_thread" : }
            bash_commande = command(options)
            timeout = 1.
            execute(bash_command,timeout)
        ants_score = [score() for ant in ants] 
        update_tree(tree_graph,evaporation_rate,ants,ants_score,ranking_function)
