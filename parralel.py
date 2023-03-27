import numpy as np
from mpi4py import MPI
from exec_algo import command, execute
import random


def paralel(l_para,comm, NbP,Me, prob, timeout):
    """argument : list de liste de parametre à tester, nb machine, machine rank, liste/tuple de trois entier representant la taille du problem
    calcul le score de chaque chemin avec des calculs paralleles
    retourne une liste de tuple [(chemin,score)]"""

    if Me==0:
        print(f"Nombre de sparks de la generation : {len(l_para)}")
        liste_para=resize(l_para,NbP)
        nbTot=len(liste_para)
        nbLoc=nbTot//NbP
        data=liste_para
    else :
        data=None
    print(f"Machine : {Me}  data : {data}")
    data=comm.scatter(data,root=0)

    #Calcul

    data_score=get_score(data,prob,timeout)

    #Envoie vers le root
    
    data_score_tot=comm.gather(data_score,root=0)

    return data_score_tot



def resize(l_p,nb_part):
    """ajoute un certain nombre de None dans la liste afin d'obtenir une taille de liste 
    multiple de nb_part
    retourne un array"""

    #Suppression des doublons
    l=unique(l_p)

    r=len(l)%nb_part
    ajout=nb_part-r
    resized_l=l.copy()
    for i in range(ajout):
        resized_l.append(None)
    random.shuffle(resized_l)
    l_sous_liste=len(resized_l)//nb_part
    cut_l=[[resized_l[i*l_sous_liste:(i+1)*l_sous_liste-1] for i in range(nb_part)]]

    return cut_l


def get_score(l_param,prob,timeout):
    """parametre = liste de liste de paramatre pour iso3d
    retourne une liste de tuple de la forme : [(sim_para,score),(..,..)]"""

    l_score=[]

    for sim_para in l_param:
        score=execute(
                                command(
                                    {
                                        "filename": "../iso3dfd-st7/compiled/bin_"
                                        + sim_para[0]
                                        + "_"
                                        + sim_para[1]
                                        + ".exe",
                                        "size1": str(prob[0]),
                                        "size2": str(prob[1]),
                                        "size3": str(prob[2]),
                                        "num_thread": str(sim_para[2]),
                                        "dim1": str(sim_para[3]),
                                        "dim2": str(sim_para[4]),
                                        "dim3": str(sim_para[5]),
                                    }
                                ),
                                timeout,
                            )
        l_score.append((sim_para,score))
    return l_score


def unique(l):
    l_unique=[]
    for i in l :
        if i not in l_unique:
            l_unique.append(i)
    return l_unique