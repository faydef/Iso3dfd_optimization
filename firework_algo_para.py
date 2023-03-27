import random
import numpy as np
from exec_algo import command, execute
import time
from parralel import paralel
from mpi4py import MPI


comm = MPI.COMM_WORLD
NbP = comm.Get_size()
Me = comm.Get_rank()


timeout = 30

problem=[128,128,128]

"parametre : Olevel, avx, nb thread, n1,n2,n3"

attributs=[["O1","O2","O3","Ofast"],
       ["sse","avx","avx2","avx512"],
       [i for i in range(1,33)],
       [16*i for i in range(1,round(problem[0]/16))],
       [i for i in range(1,problem[1]+1)],
       [i for i in range(1,problem[2]+1)]
       ]

dim=6

"""On utlise un espace continue de dimension 512^6 que l'on va découper"""

def loc_to_attribut(loc):
    """parametre list of float in range 512, NO SCORE"""
    att=[]
    for i in range(len(loc)):
        att_indexe=int(loc[i]//(problem[0]/len(attributs[i])))
        att.append(attributs[i][att_indexe])
    return att


saved_config={}
eco=0

eps=1

def firework(n,a,b,distance,m,m_gauss,A,NbP,Me,prob,timeout):
    """parametre : 
    n : number of initial fireworks
    a : minimum rate sparks/firework
    b : maximum rate spark/firework
    distance : distance function between sparks (Manhatan, Euleur,...)
    m : total number of sparks generated by n fireworks
    A : maiximum explosion amplitude
    
    loc_score is of the form : 
    firework/spark_score = [[spark/firework, score], ...]
    firework/spark = [Olevel, avx, nb thread, n1,n2,n3]
    """

    if Me==0:
        bests=[]

        count=0
        fireworks=initiate(n)
        fireworks_score=get_spark_score(fireworks,NbP,Me,prob,timeout)

    while count < 5: #stop criteria, here, the loop go through 5 times
        if Me==0:
            sparks_exp=explosion(fireworks_score,a,b,m,A,n)
            sparks_gauss=gaussian_spark(fireworks_score,m_gauss)
            sparks=sparks_exp+sparks_gauss
            sparks_score=get_spark_score(sparks,NbP,Me,prob,timeout)
            fireworks_score=new_fireworks(sparks_score,n,distance)

            count+=1
            best=best_loc(sparks_score)
            print(loc_to_attribut(best[0]),best[1])
            bests.append((loc_to_attribut(best[0]),best[1]))

        else : 
            sparks=None
            sparks_score=get_spark_score(sparks,NbP,Me,prob,timeout)

    if Me==0:
        print(bests)
        best=best_loc(sparks_score)
        return loc_to_attribut(best[0]),best[1]


def initiate(n):
    """Select n random point"""
    fireworks=[]
    for i in range(n):
        f=[]
        for d in range(dim):
            f.append(random.uniform(0,problem[0]))
        fireworks.append(f)
    return fireworks


def explosion(fireworks_score,a,b,m,A,n):
    """return a list of spark"""
    indexes=[i for i in range(dim)]
    number_spark_per_firework=[]
    amplitude_per_firework=[]

    best_score=best_loc(fireworks_score)
    worst_score=worst_loc(fireworks_score)

    denom_nb=n*best_score[1]-sum([i[1] for i in fireworks_score])+eps
    denom_A = sum([i[1] for i in fireworks_score])-n*worst_score[1]+eps
    for fs in fireworks_score:
        uncapped_n_spark=m*(fs[1]-worst_score[1]+eps)/denom_nb
        if uncapped_n_spark<a*m:
            number_spark_per_firework.append(round(a*m))
        elif uncapped_n_spark>b*m:
            number_spark_per_firework.append(round(b*m))
        else:
            number_spark_per_firework.append(round(uncapped_n_spark))

        amplitude_per_firework.append(A*(best_score[1]+fs[1]+eps)/denom_A)    
  

    sparks=[]
    for f in range(len(fireworks_score)):
        for i in range(number_spark_per_firework[f]):
            s=fireworks_score[f][0].copy()
            z=random.randrange(dim)
            attribute_indexes=random.choices(indexes,k=z)
            deplacement = amplitude_per_firework[f]*random.uniform(-1,1)
            for att in attribute_indexes:
                s[att]=s[att]+deplacement
                if 0>s[att] or s[att]>problem[0]:
                    s[att]=s[att]%problem[0]
            sparks.append(s)

    return sparks


def gaussian_spark(firework_scores,m_gauss):
    indexes=[i for i in range(dim)]
    sparks=[]
    for m in range(m_gauss):
        s=random.choice(firework_scores)[0].copy()
        z=random.randrange(dim)
        attribute_indexes=random.choices(indexes,k=z)
        g=random.gauss(1,1)
        for a in attribute_indexes:
            s[a]=s[a]*g
            if 0>s[a] or s[a]>problem[0]:
                s[a]=s[a]%problem[0]
        sparks.append(s)
    return sparks


def get_spark_score(sparks,NbP,Me, prob, timeout):

    return paralel(sparks,NbP,Me,prob,timeout)

    """
    score_sparks=[]
    n_spark=len(sparks)
    print(f"Nombre de sparks dans cette generation : {n_spark}")
    compteur=0
    for s in sparks :
        att_val=loc_to_attribut(s)
        if ''.join(str(e) for e in att_val) not in saved_config.keys():
            score=execute(
                                command(
                                    {
                                        "filename": "../iso3dfd-st7/compiled/bin_"
                                        + att_val[0]
                                        + "_"
                                        + att_val[1]
                                        + ".exe",
                                        "size1": str(problem[0]),
                                        "size2": str(problem[1]),
                                        "size3": str(problem[2]),
                                        "num_thread": str(att_val[2]),
                                        "dim1": str(att_val[3]),
                                        "dim2": str(att_val[4]),
                                        "dim3": str(att_val[5]),
                                    }
                                ),
                                timeout,
                            )
            score_sparks.append((s,score))
            saved_config[''.join(str(e) for e in att_val)]=score
        compteur+=1
        if compteur%10==0:
            print(compteur)"""
    return score_sparks


def new_fireworks(sparks_score,n,distance):
    distance_spark=[]
    for s in sparks_score :
        Rs=0
        for s2 in sparks_score:
            Rs+=distance(s[0],s2[0])
        distance_spark.append(Rs)

    proba_spark=[]
    total_R=sum(distance_spark)
    for R in distance_spark:
        proba_spark.append(R/total_R)

    fireworks_score = random.choices(sparks_score,weights=proba_spark,k=n-1)
    fireworks_score.append(best_loc(sparks_score))
    return fireworks_score


def euclide(loc1,loc2):
    """take two location without score"""
    d=0
    for i in range(len(loc1)):
        d+=(loc1[i]-loc2[i])**2
    return np.sqrt(d)


def best_loc(loc_score):
    best= max(loc_score, key=lambda item:item[1])
    return best

def worst_loc(loc_score):
    return min(loc_score, key=lambda item:item[1])


print(firework(5,0.04,0.8,euclide,50,5,60, NbP,Me,problem,timeout))

"""
f1 = main(5,0.04,0.8,euclide,50,5,40)
f2 = main(7,0.04,0.8,euclide,50,5,40) #plus fireworks
f3 = main(5,0.04,0.8,euclide,50,5,60) #plus large 
f4 = main(5,0.04,0.8,euclide,50,10,40) #plus gauss
f5 = main(5,0.04,0.8,euclide,60,5,60) #plus sparks et plus etendu

fs=[f1,f2,f3,f4,f5]

for i in range(5):
    print(f"-----f{i}-----")
    print(fs[i])"""
