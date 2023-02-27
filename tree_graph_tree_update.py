def update_tree(tree,evaporation_rate,ants,ants_score,ranking_function):
    """return the updated tree with the score of the previous ant, the decay of the present pheromone and
    the choice of the cost function"""
    
    pheromone_decay(tree,evaporation_rate) 

    pheromone_added = ranking_function(ants,ants_score)
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



def average_ranking_function(ants,ants_score,maybe_other_argument=None):
    """Must return a list of number corresponding to the amount of pheromone that have to be
       added to the tree and the corresponding path
       returned list are [pheromone, path] where path is a list
       """
    
    return [0,[]]



def ASrank(ants,ants_scores, k):
    """At the end of each iteration, all solutions are ranked and the first k ant add pheromone to their path"""
    
    return []


def ElitistAS(ant,ants_score):
    """At the end of each iteration, the winner ant is rewarded"""

    return []

def MinMaxAS(ants,ants_score,min,max):
    """At the end of each iteration, the winner ant is rewarded"""

    return []