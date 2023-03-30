import random
import numpy as np
from exec_algo import command, execute
import time


"parametre : Olevel, avx, nb thread, n1,n2,n3"
"""On utlise un espace continue de dimension 512^6 que l'on va découper"""


def loc_to_attribut(loc,problem):
    """parametre list of float in range 512, NO SCORE"""

    attributs = [
    ["O1", "O2", "O3", "Ofast"],
    ["sse", "avx", "avx2", "avx512"],
    [i for i in range(1, 33)],
    [16 * i for i in range(1, round(problem[0] / 16))],
    [i for i in range(1, problem[1] + 1)],
    [i for i in range(1, problem[2] + 1)]
    ]
    att = []
    for i in range(len(loc)):
        att_indexe = int(loc[i] // (problem[0] / len(attributs[i])))
        att.append(attributs[i][att_indexe])
    return att


saved_config = {}
eps = 1E-4


def firework(n, a, b, distance, m, m_gauss, A, problem=[512,512,512], timeout=30,iteration = 5):
    """parametre : 
    n : number of initial fireworks
    a : minimum rate sparks/firework
    b : maximum rate spark/firework
    distance : distance function between sparks (Manhatan, Euclide,...)
    m : total number of sparks generated by n fireworks
    m_gauss : number of sparks generated by gaussian distribution
    A : maximum explosion amplitude
    
    loc_score is of the form : 
    firework/spark_score = [[spark/firework, score], ...]
    firework/spark = [Olevel, avx, nb thread, n1,n2,n3]
    """

    file_name=f"{problem[0]}_cube_{iteration}_iteration_result_corr.txt" #A modifier à chaque exec

    file=open(file_name,"w")
    file.close()

    start_time=time.time()
    bests = []

    count = 0
    fireworks = initiate(n,problem)
    if problem[0]==512:
        fireworks_score = get_spark_score(fireworks,problem, 60)
    else :
        fireworks_score = get_spark_score(fireworks,problem, timeout)
    end_time=time.time()
    save_result(file_name,fireworks_score,end_time-start_time,0,problem)
    while count < iteration:  # stop criteria, here, the loop went through 5 times
        start_time=time.time()
        sparks_exp = explosion(fireworks_score, a, b, m, A, n, problem)
        sparks_gauss = gaussian_spark(fireworks_score, m_gauss,problem)
        sparks = sparks_exp + sparks_gauss
        sparks_score = get_spark_score(sparks,problem,timeout)
        sparks_score.append(best_loc(fireworks_score))
        if distance == "euclide":
            fireworks_score = new_fireworks(sparks_score, n, euclide)

        count += 1
        best = best_loc(sparks_score)
        print(loc_to_attribut(best[0],problem), best[1])
        bests.append((loc_to_attribut(best[0],problem), best[1]))

        end_time=time.time()
        save_result(file_name,sparks_score,end_time-start_time,count,problem)

    print(bests)
    best = best_loc(sparks_score)
    return loc_to_attribut(best[0],problem), best[1]


def initiate(n,problem):
    """Select n random point"""
    fireworks = []
    for i in range(n):
        f = []
        for d in range(6):
            f.append(random.uniform(0, problem[0]))
        fireworks.append(f)
    return fireworks


def explosion(fireworks_score, a, b, m, A, n,problem):
    """return a list of spark"""
    indexes = [i for i in range(6)]
    number_spark_per_firework = []
    amplitude_per_firework = []

    best_score = best_loc(fireworks_score)
    worst_score = worst_loc(fireworks_score)

    denom_A = sum([best_score[1]-i[1] for i in fireworks_score]) + eps
    denom_nb = sum([i[1]-worst_score[1] for i in fireworks_score]) + eps
    for fs in fireworks_score:
        uncapped_n_spark = m * (fs[1] - worst_score[1] + eps) / denom_nb
        if uncapped_n_spark < a * m:
            number_spark_per_firework.append(round(a * m))
        elif uncapped_n_spark > b * m:
            number_spark_per_firework.append(round(b * m))
        else:
            number_spark_per_firework.append(round(uncapped_n_spark))

        amplitude_per_firework.append(A *(best_score[1] - fs[1] + eps) / denom_A)


    sparks = []
    for f in range(len(fireworks_score)):
        for i in range(number_spark_per_firework[f]):
            s = fireworks_score[f][0].copy()
            z = random.randrange(6)
            attribute_indexes = random.choices(indexes, k=z)
            deplacement = amplitude_per_firework[f] * random.uniform(-1, 1)
            for att in attribute_indexes:
                s[att] = s[att] + deplacement
                if 0 > s[att] or s[att] > problem[0]:
                    s[att] = s[att] % problem[0]
            sparks.append(s)

    return sparks


def gaussian_spark(firework_scores, m_gauss, problem):
    indexes = [i for i in range(6)]
    sparks = []
    for m in range(m_gauss):
        s = random.choice(firework_scores)[0].copy()
        z = random.randrange(6)
        attribute_indexes = random.choices(indexes, k=z)
        g = random.gauss(1, 1)
        for a in attribute_indexes:
            s[a] = s[a] * g
            if 0 > s[a] or s[a] > problem[0]:
                s[a] = s[a] % problem[0]
        sparks.append(s)
    return sparks


def get_spark_score(sparks,problem,timeout):
    score_sparks = []
    n_spark = len(sparks)
    print(f"Nombre de sparks dans cette generation : {n_spark}")
    compteur = 0
    for s in sparks:
        att_val = loc_to_attribut(s,problem)
        if "".join(str(e) for e in att_val) not in saved_config.keys():
            score = execute(
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
            score_sparks.append((s, score))
            saved_config["".join(str(e) for e in att_val)] = score
        compteur += 1
        if compteur % 10 == 0:
            print(compteur)
    return score_sparks


def new_fireworks(sparks_score, n, distance):
    distance_spark = []
    for s in sparks_score:
        Rs = 0
        for s2 in sparks_score:
            Rs += distance(s[0], s2[0])
        distance_spark.append(Rs)

    proba_spark = []
    total_R = sum(distance_spark)
    for R in distance_spark:
        proba_spark.append(R / total_R)

    fireworks_score = random.choices(sparks_score, weights=proba_spark, k=n - 1)
    fireworks_score.append(best_loc(sparks_score))
    return fireworks_score


def euclide(loc1, loc2):
    """take two location without score"""
    d = 0
    for i in range(len(loc1)):
        d += (loc1[i] - loc2[i]) ** 2
    return np.sqrt(d)


def best_loc(loc_score):
    best = max(loc_score, key=lambda item: item[1])
    return best


def worst_loc(loc_score):
    return min(loc_score, key=lambda item: item[1])

def mean_loc(loc_score):
    scores=[i[1] for i in loc_score]
    return sum(scores)/len(scores)

def save_result(file_name,loc_score,exec_time,iteration_number,prob):
    """write in a file file_name the results of the firework optimisation algo
    results are : for each iteration, best loc, Gflops of best, means of GFlops, execution time of the iteration
    Call this function at each iteration"""
    with open(file_name,"a") as file:
        if iteration_number==0:
            file.write("\nInitialisation\n")
        else :
            file.write(f"\nIteration num : {iteration_number}\n")
        file.write(f"Moyenne de Gflops sur l'iteration : {mean_loc(loc_score)}\n")
        best=best_loc(loc_score)
        file.write(f"Meilleur Gflops sur l'iteration : {best[1]}\n")
        file.write(f"Parametre du meilleur résultat : {loc_to_attribut(best[0],prob)}\n")
        file.write(f"iteration executé en {exec_time}s\n")


# Best config firework(5,0.04,0.8,"euclide",50,5,60)

firework(5,0.04,0.8,"euclide",50,5,60, problem=[128,128,128],timeout=30,iteration=10)
firework(5,0.04,0.8,"euclide",50,5,90, problem=[128,128,128],timeout=30,iteration=10)
firework(5,0.04,0.8,"euclide",50,5,120, problem=[128,128,128],timeout=30,iteration=10)
#firework(5,0.04,0.8,"euclide",50,5,60, problem=[256,256,256],timeout=30,iteration = 7)

#firework(5,0.04,0.8,"euclide",50,5,60, problem=[512,512,512],timeout=40,iteration=10)

#firework(5,0.04,0.8,"euclide",50,5,60, problem=[512,512,512],timeout=40,iteration=9)

#firework(5,0.04,0.8,"euclide",50,5,60, problem=[512,512,512],timeout=40,iteration=8)