def update_tree(tree, evaporation_rate, ants, ants_score, minMax=False, max_pheromone=100, min_pheromone=0):
    """return the updated tree with the score of the previous ant, the decay of the present pheromone and
    the choice of the cost function
    If minMax = False, will not use the minmax pheromone attribution method, if true, take care to tune
    the max_pheromone and min_pheromone parameters
    """
    
    pheromone_decay(tree,evaporation_rate,minMax,min_pheromone)
    score_path=zip(ants_score,ants)
    pheromone_added = ASrank(score_path,20,1) #Choose here which ranking function to use, the one that exist are are the end of the file
    add_pheromone(tree,pheromone_added, minMax, max_pheromone)

    pheromone_decay(tree, evaporation_rate, minMax, min_pheromone)
    score_path = list(zip(ants_score, ants))
    # Choose here which ranking function to use, the one that exist are are the end of the file
    pheromone_added = ASrank(score_path, 20, 1)
    add_pheromone(tree, pheromone_added, minMax, max_pheromone)


def pheromone_decay(tree, evaporation_rate, minMax, min_pheromone):
    """modify the tree after the pheromone rate decreased"""

    for key, value in tree.items():
        if key == 0:
            tree[key] = (1-evaporation_rate)*value
            if minMax and tree[key] < min_pheromone:
                tree[key] = min_pheromone
        else:
            pheromone_decay(tree[key], evaporation_rate, minMax, min_pheromone)


def add_pheromone(tree, new_pheromone, minMax, max_pheromone):
    """new_pheromone should be list such as [added_pheromone,path] where path is a list"""

    def add_to_next_node(pheromone, child_tree, path):
        if len(path) > 0:
            next_node = path.pop(0)
            child_tree[next_node][0] += pheromone
            if minMax and child_tree[next_node][0] > max_pheromone:
                child_tree[next_node][0] = max_pheromone
            add_to_next_node(pheromone, child_tree[next_node], path)

    for pheromone_path in new_pheromone:
        add_to_next_node(pheromone_path[0], tree, pheromone_path[1])


def ants_ants_score_merge(ants, ants_score):
    path_score = []
    for i in range(len(ants)):
        try:
            path_score.append([ants_score[i], ants[i]])
        except IndexError:
            print("Le nombre de score et de fourmis diffèrent")
    return path_score


def ASrank(score_path, k, pheromone_added):
    """At the end of each iteration, all solutions are ranked and the first k ant add pheromone to their path"""
    score_path.sort(
        key=lambda x: x[0], reverse=False)  # Peut etre changer reverse en fonction du cout
    k_best = score_path[:k]
    pheromone_path = [[pheromone_added, k_best[i][1]]
                      for i in range(len(k_best))]
    return pheromone_path


def BestAnt(score_path):
    """Return the best ant of the iteration"""
    best_ant = max(score_path, key=lambda x : x[0]) #Peut etre min en fonction du cout
    return best_ant
