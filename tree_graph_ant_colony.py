import random

def exploration(tree,nb_ant,list_dict_parameters):
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
        ants.append(choose_path(tree,list_dict_parameters))

    return ants



def choose_child_node(parent,list_dict_parameters,depth):
    """Choose a child node depending on the parent node and thus, the pheromone
    return the under_tree taking the child choosen as the root"""

    children=get_children_list(parent)

    child_weight = [parent[child][0] for child in children]
    
    child_name = random.choices(children, weights=child_weight, k=1)[0]

    return parent[child_name],list_dict_parameters[depth][child_name]


def choose_path(tree,list_dict_parameters):
    """return a list corresponding the the path taken by an ant"""

    current_parent=tree.copy()
    path=[]
    depth = 0
    while len(current_parent)>1:
        current_parent,child_name=choose_child_node(current_parent,list_dict_parameters,depth)
        path.append(child_name)
        depth+=1

    return path


def get_children_list(parent):
    """return the list of children of one node"""

    parent_keys = list(parent.keys())

    if 0 in parent_keys:
        parent_keys.remove(0)
    
    return parent_keys
