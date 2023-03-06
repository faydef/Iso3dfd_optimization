

def tree_generation(compil_flag_list, simd_list, num_threads_max, n1_size, n2_size, n3_size):
    """Returns a tree in the form of dictionnaries of dictionnaries of ... with branches for every choice of the following parameters:
    -Olevel -simd -num_threads -n1_block -n2_block -n3_block"""
    tree_graph = {"pheromone_rate": 0}

    list_n1block = values_nblock(n1_size, first=True)
    list_n2block = values_nblock(n2_size, first=False)
    list_n3block = values_nblock(n3_size, first=False)

    list_num_thread = values_num_thread(num_threads_max)

    list_ordered_of_parameters = list_of_parameters(
        compil_flag_list, simd_list, list_num_thread, list_n1block, list_n2block, list_n3block)

    tree_graph = add_children(
        tree_graph, list_ordered_of_parameters, 0)

    return tree_graph


def values_nblock(n_size, first):
    """return list of integers corresponding to all the possibilities
    of nk_block corresponding to a certain nk size for the problem
    if using for n1block then set first = True else set first = False"""
    list_nblock = []
    if first:
        if n_size >= 2:
            list_nblock.append('2')
        if n_size >= 4:
            list_nblock.append('4')
        if n_size >= 8:
            list_nblock.append('8')
        i = 1
        while n_size >= (16*i):  # add all multiples of 16 smaller than n_size
            a = 16*i
            list_nblock.append(str(a))
            i += 1
    else:
        list_nblock = range(1, n_size+1)

    return list_nblock


def values_num_thread(num_threads_max, type='power_of_2'):
    """return list of integers corresponding to all the possibilities
    of num_threads based on the maximum number of threads.
    The list contains the powers of 2 dividing the num_threads_max if type = str(power_of_2) and by default,
    can also contain all the numbers under the maximum number of threads if type = str(all)"""
    list_num_thread = []
    if type == 'power_of_2':
        i = 1
        while num_threads_max//(2 ** i) != 0:
            a = 2**i
            list_num_thread.append(str(a))
            i += 1
    if type == 'all':
        list_num_thread = range(1, num_threads_max + 1)
    return list_num_thread


def list_of_parameters(compil_flag_list, simd_list, list_num_thread, list_n1block, list_n2block, list_n3block, order='default'):
    """returns the list of list of parameters with an order you can choose by default returns the list in the following order:
      compil_flag_list, simd_list, list_num_thread, list_n1block, list_n2block, list_n3block"""
    if order == 'default':
        return [compil_flag_list, simd_list, list_num_thread, list_n1block, list_n2block, list_n3block]


def add_children(parent_tree, list_ordered_of_parameters, depth, pheromone_rate_repartition_list=['even']):
    """return parent tree with children tree added recursively for a certain list of parameters,
    can take a pheromone rate repartition by default evenly spread the pheromones on all children """
    if depth >= len(list_ordered_of_parameters):
        return parent_tree
    list_values_of_parameter = list_ordered_of_parameters[depth]

    pheromone_rate_repartition = pheromone_rate_repartition_list[0]
    if pheromone_rate_repartition == 'even':
        pheromone_rate_value = 1/len(list_values_of_parameter)

    for parameter_value in list_values_of_parameter:
        parent_tree[parameter_value] = {
            'pheromone_rate': pheromone_rate_value}
        add_children(
            parent_tree[parameter_value], list_ordered_of_parameters, depth + 1)
    return parent_tree


def remove_pheromons(tree_graph):
    """return tree without pheromone to enable it to be a graph for any python library enabling us to plot the tree
    we have yet to find a way to plot it"""
    del tree_graph["pheromone_rate"]
    if tree_graph == {}:
        return tree_graph
    for value in tree_graph.values():
        remove_pheromons(value)
    return tree_graph
