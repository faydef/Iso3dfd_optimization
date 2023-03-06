#coding:utf-8

from tree_graph_generation import *
from tree_graph_ant_colony import *
from tree_graph_tree_update import *
from exec_algo import *


def ask_for(question,default_value):
    res = input(question)
    if res == "" :
        return default_value
    else :
        return res


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
nb_ants = ask_for("number of ants per iteration : ",10)
evaporation_rate = ask_for("evaporation_rate : ",0)
n1_size = ask_for("size of the problem x : ",256)
n2_size = ask_for("size of the problem y : ",256)
n3_size = ask_for("size of the problem z : ",256)
n_threads_max = ask_for("maximum number of threads : ",32)


list_num_thread = values_num_thread(n_threads_max)


#print(n_size)
#print(n_threads_max)


if type_algo == 1 :
    tree_graph = tree_generation(compil_flag_list,simd_list,n_threads_max,n1_size,n2_size,n3_size)

    for _ in range(nb_iter):    
        ants = exploration(tree_graph,nb_ants)
        ants_score = []
        for ant in ants :
            olevel = ant[0]
            simd = ant[1]
            num_threads = str(ant[2])
            dim1 = str(ant[3])
            dim2 = str(ant[4])
            dim3 = str(ant[5])
            filename = "bin_{}_{}.exe".format(simd,olevel)
            options = {"filename" : filename, "size1":str(n1_size),"size2":str(n2_size),"size3":str(n3_size),\
                    "num_thread" : str(num_threads), "dim1":str(dim1), "dim2":str(dim2),"dim3":str(dim3)}
            bash_command = command(options)
            timeout = 30.
            score = execute(bash_command,timeout)
            ants_score.append(score)

        update_tree(tree_graph,evaporation_rate,ants,ants_score)
