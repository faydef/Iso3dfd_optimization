def values_nblock(n_size):
    """return list of integers corresponding to all the possibilities 
    of nk_block corresponding to a certain nk size for the problem"""
    list_nblock = []
    if n_size >= 2:
        list_nblock.append(2)
    if n_size >= 4:
        list_nblock.append(4)
    if n_size >= 8:
        list_nblock.append(8)

    i = 1
    while n_size >= (16*i):
        list_nblock.append(16*i)  # add all multiples of 16 smaller than n_size
        i += 1

    return list_nblock


def values_num_thread_power_of_2(num_threads_max):
    """return list of integers corresponding to all the possibilities 
    of num_threads based on the maximum number of threads.
    The list contains the powers of 2 dividing the num_threads_max"""
    list_num_thread = []
    i = 1
    while num_threads_max//(2 ^ i) != 0:
        list_num_thread.append(2 ^ i)
        i += 1
    return list_num_thread


def list_of_parameters(compil_flag_list, simd_list, list_num_thread, list_n1block, list_n2block, list_n3block, order='default'):
    """returns the list of list of parameters with an order you can choose by default returns the list in the following order:
      compil_flag_list, simd_list, list_num_thread, list_n1block, list_n2block, list_n3block"""
    if order == 'default':
        return [compil_flag_list, simd_list, list_num_thread, list_n1block, list_n2block, list_n3block]


def add_child_dictionnaries(parent_dictionnary, list_ordered_of_parameters, pheromone_rate_repartition_list=['even']):
    """return parent dictionnary with child dictionnaries added recursively for a certain list of parameters, 
    can take a pheromone rate repartition by default evenly spread the pheromons on all children """
    if list_ordered_of_parameters == []:
        return parent_dictionnary
    pheromone_rate_repartition = pheromone_rate_repartition_list.pop(0)
    if pheromone_rate_repartition == 'even':
        pheromone_rate_value = 1/len(list_values_of_parameter)
    list_values_of_parameter = list_ordered_of_parameters.pop(0)
    for value in list_values_of_parameter:
        parent_dictionnary[value] = {'pheromone_rate': pheromone_rate_value}
    return add_child_dictionnaries(parent_dictionnary, list_ordered_of_parameters)


def tree_generation(compil_flag_list, simd_list, num_threads_max, n1_size, n2_size, n3_size):
    """Returns a tree in the form of dictionnaries of dictionnaries of ... with branches for every choice of the following parameters:
    -Olevel -simd -num_threads -n1_block -n2_block -n3_block"""
    tree_graph = {"pheromone_rate": 0}

    list_n1block = values_nblock(n1_size)
    list_n2block = values_nblock(n2_size)
    list_n3block = values_nblock(n3_size)
    list_num_thread = values_num_thread_power_of_2(num_threads_max)
    list_ordered_of_parameters = list_of_parameters(
        compil_flag_list, simd_list, list_num_thread, list_n1block, list_n2block, list_n3block)

    tree_graph = add_child_dictionnaries(
        tree_graph, list_ordered_of_parameters)

    return tree_graph


if __file__ == "main":  # small tests
    tree_graph = tree_generation(["O3", "O2", "Ofast"], [
                                 "avx2", "avx512"], 16, 2, 2, 2)
    print(tree_graph)
