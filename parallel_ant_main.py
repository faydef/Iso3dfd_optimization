from representation import initiate
from update import update      
from exec_algo import command, execute
import numpy as np
from random import choices
from operator import itemgetter
import sys
import time
import mpi4py.MPI as MPI



def execution(ants,problem,timeout):
    """
    This function executes the command line for the ants' paths.
    Parameters:
        ants    :  List of paths and the number of ants that chose each path.
        problem :  List of the problem dimensions.
        timeout :  Maximum time allowed for command line execution.

    Returns:
        ants    :  The score of each path is added to the initial list.
        timer   :  Execution time of each path (timeout if the execution time exceeds this limit).
    """
    timer = np.array([])
    ants.append([])
    for i in range(len(ants[0])):
        path = ants[0][i]
        execution = execute(
                command(
                    {
                        "filename": "../iso3dfd-st7/compiled/bin_"
                        + path[0]
                        + "_"
                        + path[1]
                        + ".exe",
                        "size1": str(problem[0]),
                        "size2": str(problem[1]),
                        "size3": str(problem[2]),
                        "num_thread": str(path[2]),
                        "dim1": str(path[3]),
                        "dim2": str(path[4]),
                        "dim3": str(path[5]),
                    }
                ),
                timeout,
            )
        ants[2].append(execution[0])
        timer = np.append(timer, execution[1])
    return ants,timer


def ant(nb_ant, liste, dico, worst):
    """
    This function is for selecting paths randomly in the root process.
    Parameters:
        nb_ant : Number of ants.
        liste  : List of choices for each variable in the path.
        dico   : Dictionary of probability weights for making random choices.
        worst  : Set of the worst paths to avoid.
    Returns:
        ants : List of paths and the number of ants that chose each path.
    """
    ##########################################initiate the ants###########################################
    ants = [
        [],
        []
    ]  # liste of paths, number of ants that choosed this path
    for i in range(nb_ant):
        ######################################choose randomly a path to explore based on probability weights##############################
        safe_path = True
        while safe_path:
            path_choices = {}
            path_choices[f'choice_{1}'] = choices(
                    liste[f'liste{1}'],
                    weights = dico[f'mat{1}'],
                    k=1,
            )[0]
            for i in range(2,7):
                path_choices[f'choice_{i}'] = choices(
                    liste[f'liste{i}'],
                    weights = dico[f'mat{i}'][liste[f'liste{i-1}'].index(path_choices[f'choice_{i-1}'])],
                    k=1,
                )[0]
                
            path = []
            for i in range(6):
                path.append(path_choices[f'choice_{i+1}'])
            
            if not (tuple(path) in worst):
                safe_path = False
        ##########################################store the path###########################################
        # if the path is already explored we increment the number of ants
        if path in ants[0]:
            ants[1][ants[0].index(path)] += 1
        # else we add the path to the list of paths and we excute the command line and store its Gflops and time execution
        else:
            ants[0].append(path)
            ants[1].append(1)
    return ants

def divide_list_to_ranks(data, size):
    """
    This function divides a list into chunks so that each chunk can be sent to a separate process.
        Parameters:
            data : The data to divide into chunks.
            size : Number of processes.

        Returns:
            chunks : List of lists to send to each process.
    """
    chunk_size = len(data) // size
    extra = len(data) % size
    chunks = []
    start = 0
    
    for i in range(size):
        end = start + chunk_size
        if i < extra:
            end += 1
        chunks.append(data[start:end])
        start = end

    return chunks

if __name__ == "__main__":
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        (
            _,
            nb_ant,
            nb_iteration,
            problem_1,
            problem_2,
            problem_3,
            rho,
            alpha,
            Q,
            timeout,
        ) = sys.argv
        if timeout == 'auto':
            timeout = execute(
                command(
                    {
                        "filename": "../iso3dfd-st7/compiled/bin_"
                        + "O2"
                        + "_"
                        + "avx"
                        + ".exe",
                        "size1": problem_1,
                        "size2": problem_2,
                        "size3": problem_3,
                        "num_thread": "32",
                        "dim1": str(16),
                        "dim2": str(16),
                        "dim3": str(16),
                    }
                )
            )[1]
            add = max(1,0.3*timeout)
            timeout += add
        print("the initial timeout: "+str(timeout))
        # inputs argument to brodcast
        input_args = (
            int(nb_ant),
            int(nb_iteration),
            [int(problem_1), int(problem_2), int(problem_3)],
            float(rho),
            float(alpha),
            float(Q),
            int(timeout),
        )
        problem = input_args[2]
        liste, dico = initiate(problem)  # list of choices and there probability
        best = [[], 0]  # store the best solution with its Gflops
        worst = set()  # set of worst path to avoid them
    else:
        input_args = None
    
    # Broadcast input_args to all processes
    input_args = comm.bcast(input_args, root=0)
    timeout = input_args[6]
        
    for j in range(input_args[1]):
        if rank == 0:
            print("############interation "+str(j+1)+'/'+str(input_args[1])+'     Q='+Q)
            ants = ant(input_args[0], liste, dico, worst)
            divided_paths = divide_list_to_ranks(ants[0],size)
            divided_num = divide_list_to_ranks(ants[1],size)
            local_ants = [[divided_paths[i],divided_num[i]] for i in range(size)]
        else:
            local_ants = None
        
        local_ants = comm.scatter(local_ants, root=0)
        comm.Barrier()
        
        #execute line command
        
        ants, timer = execution(local_ants, input_args[2], timeout)
        comm.Barrier()
        

        local_timer_length = len(timer)
        counts = comm.gather(local_timer_length,root=0)
        
        displacements = None
        gathered_timer = None

        if rank == 0:
            total_size = sum(counts)
            gathered_timer = np.empty(total_size, dtype=np.float64)
            displacements = np.zeros(size, dtype=int)
            np.cumsum(counts[:-1],out=displacements[1:])
        
        comm.Gatherv(timer,[gathered_timer,counts,displacements,MPI.DOUBLE], root=0)
        comm.Barrier()

        #gather the ants so we can update probability
        gathered_paths = comm.gather(ants[0],root=0)
        gathered_counts = comm.gather(ants[1],root=0)
        gathered_scores = comm.gather(ants[2],root=0)
        
        
        if rank == 0 :
            # Concatenate the gathered lists
            all_paths = [path for sublist in gathered_paths for path in sublist]
            all_counts = [count for sublist in gathered_counts for count in sublist]
            all_scores = [score for sublist in gathered_scores for score in sublist]
            # Combine the concatenated lists into the final ants list
            all_ants = [all_paths, all_counts, all_scores]
            print("maximum occurrence :" + str(max(all_ants[1])))
            
        comm.Barrier()
        
        timeout_buffer = np.empty(1, dtype=int)
        if rank == 0:   
            timeout = 0
            for i in range(len(gathered_timer)):
                timeout += all_ants[1][i] * gathered_timer[i]
            timeout = int(timeout / int(nb_ant)) + 1
            timeout_buffer[0] = timeout 
            print('iteration '+str(j+1) +':'+str(timeout))    
        
        # Broadcast the timeout value from the root process
        comm.Bcast(timeout_buffer, root=0)

        # Extract the timeout value in all processes
        timeout = timeout_buffer[0]
        comm.Barrier()
            
        if rank == 0:  
            # update the probability weight for the best 10 solution
            all_ants[0], all_ants[1], all_ants[2] = map(
                list,
                zip(
                    *sorted(zip(all_ants[0], all_ants[1], all_ants[2]), key=itemgetter(2), reverse=True)
                ),
            )
            routes = [
                (all_ants[0][i], all_ants[1][i], all_ants[2][i]) for i in range(min(10, len(all_ants[0])))
            ]
            update(routes, liste, dico, input_args[3], input_args[4], input_args[5])

                
            # store the worst path to avoid them
            if len(all_ants[0]) > 20:
                for i in range(len(all_ants[0]) - 1, len(all_ants[0]) - 10, -1):
                    worst.add(tuple(all_ants[0][i]))
                for i in range(len(all_ants[0]) - 10, 0, -1):
                    if all_ants[2][i] == -99:
                        worst.add(tuple(all_ants[0][i]))
            #plot the graph 
            scores = np.array([score for score in all_ants[2] if score!=-99])
            min_score = np.min(scores)
            max_score = np.max(scores)
            avg_score = np.mean(scores)

            print(f"Max score: {max_score}, Min score: {min_score}, Average score: {avg_score}")
            # update the best solution
            if all_ants[2][0] > best[1]:
                best = [all_ants[0][0], all_ants[2][0]]
            for elements in dico.keys():
                print("max :"+str(np.max(dico[elements]))+", min:"+str(np.min(dico[elements])))
            print(best)