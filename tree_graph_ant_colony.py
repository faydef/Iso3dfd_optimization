import random

def exploration(tree,nb_ant):
    """Take a tree and the number of ant that will explore the tree
    Return a list of ant path in the form of list of list, each list being the different argument for the execution of the program
    Tree Form : {parent1 : {child1 : {pheromone_rate : int, grandchild1 : {}, grandchild2...}, 

                            child2 : {pheromone_rate : int, grandchild1 : [{},pr], grandchild2...},
                            ....
                            pheromone_rate : int },
                parent2... : {}}


    The probability for an ant to go on a branch depends on the pheromone_rate
    """
    ants=[]

    #For each ant, we choose a path
    for ant in range(nb_ant):
        ants.append(choose_path(tree))

    return ants



def choose_child_node(parent):
    """Choose a child node depending on the parent node and thus, the pheromone
    return the under_tree taking the child choosen as the root"""

    children=get_children_list(parent)

    child_weight = [parent[child]['pheromone_rate'] for child in children]
    
    child_name = random.choices(children, weights=child_weight, k=1)[0]

    return parent[child_name],child_name


def choose_path(tree):
    """return a list corresponding the the path taken by an ant"""

    current_parent=tree.copy()
    path=[]

    while len(current_parent)>1:
        current_parent,child_name=choose_child_node(current_parent)
        path.append(child_name)

    return path


def get_children_list(parent):
    """return the list of children of one node"""

    parent_keys = list(parent.keys())

    if 'pheromone_rate' in parent_keys:
        parent_keys.remove('pheromone_rate')
    
    return parent_keys
