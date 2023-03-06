def update_tree(tree,evaporation_rate,ants,ants_score):
    """return the updated tree with the score of the previous ant, the decay of the present pheromone and
    the choice of the cost function"""
    
    pheromone_decay(tree,evaporation_rate) 

    score_path = ants_ants_score_merge(ants,ants_score)
    pheromone_added = ASrank(score_path,20,1) #Choose here which ranking function to use, at the end of the file
    add_pheromone(tree,pheromone_added)



def pheromone_decay(tree,evaporation_rate):
    """modify the tree after the pheromone rate decreased"""

    for key,value in tree.items():
        if key == 'pheromone_rate' :
            tree[key] = (1-evaporation_rate)*value
        else : pheromone_decay(tree[key],evaporation_rate)


def add_pheromone(tree,new_pheromone):
    """new_pheromone should be list such as [added_pheromone,path] where path is a list"""

    def add_to_next_node(pheromone,child_tree,path):
        if len(path)>0:
            next_node=path.pop(0)
            child_tree[next_node]['pheromone_rate'] += pheromone
            add_to_next_node(pheromone,child_tree[next_node],path)
    
    for pheromone_path in new_pheromone:
        add_to_next_node(pheromone_path[0],tree,pheromone_path[1])



def ants_ants_score_merge(ants,ants_score):
    path_score=[]
    for i in range(len(ants)):
        try:
            path_score.append([ants_score[i],ants[i]])
        except IndexError:
            print("Le nombre de score et de fourmis diffèrent")
    return path_score


def average_ranking_function(ants,ants_score,maybe_other_argument=None):
    """Must return a list of number corresponding to the amount of pheromone that have to be
       added to the tree and the corresponding path
       returned list are [pheromone, path] where path is a list
       """
    
    return [0,[]]



def ASrank(score_path, k, pheromone_added):
    """At the end of each iteration, all solutions are ranked and the first k ant add pheromone to their path"""
    score_path.sort(key = lambda x : x[0], reverse=False) #Peut etre changer reverse en fonction du cout
    k_best = score_path[:k]
    pheromone_path = [[pheromone_added,k_best[i][1]] for i in range(len(k_best))]
    return pheromone_path


def ElitistAS(score_path,pheromone_added):
    """At the end of each iteration, the winner ant is rewarded"""
    best_ant = max(score_path, key=lambda x : x[0]) #Peut etre min en fonction du cout
    return [pheromone_added,best_ant[1]]


def MinMaxAS(score_path,min,max):
    """At the end of each iteration, the winner ant is rewarded"""

    return []
