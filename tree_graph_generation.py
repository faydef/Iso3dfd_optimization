def values_nblock(n):
    """return list of integers corresponding to all the possibilities 
    of nk_block corresponding to a certain nk size for the problem"""
    return 

def values_nthread_power_of_2(num_threads_max):
    """return list of integers corresponding to all the possibilities 
    of num_threads based on the maximum number of threads.
    The list contains the powers of 2 dividing the num_threads_max"""
    list_num_thread = []
    i=1
    while num_threads_max//(2^i) !=0:
        list_num_thread.append(2^i)
        i+=1
    return list_num_thread


def tree_generation(compil_flag_list, simd_list, n1, n2, n3, num_threads_max):
    """Returns a tree in the form of dictionnaries of dictionnaries of ... with branches for every choice of parameter:
    -Olevel -simd -num_threads -num_threads -n1_block -n2_block -n3_block"""