from representation import initiate
from update import update
from exec_algo import command, execute
import numpy as np
from random import choices
from operator import itemgetter
import sys
import time
import mpi4py.MPI as MPI



def ant(worst, liste, dico, nb_ant, rho, alpha, Q, timeout, size, rank):
    """
    this function is the main function of the ant colony algorithm.
    parameters:
        nb_ant: number of ants
        nb_iteration: number of iterations
        problem: list of the dimensions of the problem
        rho: pheromone evaporation rate
        alpha: pheromone importance
        Q: pheromone deposit factor
        timeout: time limit for the command line execution
    return:
        best: best solution found
    """
    ##########################################initiate the ants###########################################
    ants = [
        [],
        [],
        [],
    ]  # liste of paths, number of ants that choosed this path and their score
    timer = np.array([])  # liste of execution time in order to update the timeout
    
    for i in range(nb_ant_per_node):
        
        
        ######################################choose randomly a path to explore based on probability weights##############################
        safe_path = True
        while safe_path:
            choices_1 = choices(liste["liste1"], weights=dico["mat1"], k=1)[0]
            choices_2 = choices(
                liste["liste2"],
                weights=dico["mat2"][liste["liste1"].index(choices_1)],
                k=1,
            )[0]
            choices_3 = choices(
                liste["liste3"],
                weights=dico["mat3"][liste["liste2"].index(choices_2)],
                k=1,
            )[0]
            choices_4 = choices(
                liste["liste4"],
                weights=dico["mat4"][liste["liste3"].index(choices_3)],
                k=1,
            )[0]
            choices_5 = choices(
                liste["liste5"],
                weights=dico["mat5"][liste["liste4"].index(choices_4)],
                k=1,
            )[0]
            choices_6 = choices(
                liste["liste6"],
                weights=dico["mat6"][liste["liste5"].index(choices_5)],
                k=1,
            )[0]
            path = [
                choices_1,
                choices_2,
                choices_3,
                choices_4,
                choices_5,
                choices_6,
            ]
            if not (tuple(path) in worst):
                safe_path = False
        
        
        
        ##########################################execute and store the path###########################################
        # if the path is already explored we increment the number of ants
        if path in ants[0]:
            ants[1][ants[0].index(path)] += 1
            
        
        # else we add the path to the list of paths and we excute the command line and store its Gflops and time execution
        else:
            ants[0].append(path)
            ants[1].append(1)
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
    return timer, ants


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

        # Broadcast the input arguments to all processes
        input_args = (
            int(nb_ant),
            int(nb_iteration),
            [int(problem_1), int(problem_2), int(problem_3)],
            float(rho),
            float(alpha),
            float(Q),
            int(timeout),
        )
    else:
        input_args = None

    # Broadcast input_args to all processes
    input_args = comm.bcast(input_args, root=0)
    
    
    ##########################################initiate the problem###########################################
    problem = input_args[2]
    liste, dico = initiate(problem)  # list of choices and there probability
    if rank == 0 :
        best = [[], 0]  # store the best solution with its Gflops
    worst = set()  # set of worst path to avoid them
    nb_ant_per_node = input_args[0] // size
    timeout = input_args[6]

    if rank < input_args[0] % size:
        nb_ant_per_node+=1
        
    for j in range(input_args[1]):
        timer, ants = ant(worst, liste, dico, nb_ant_per_node, input_args[3], input_args[4], input_args[5], timeout, size, rank)
         
        # update the timeout
        comm.Barrier()
        
        # Calculate the total length of the timer list across all processes
        timer_length = len(timer)
        counts = comm.gather(timer_length,root=0)
        
        displacements = None
        gathered_timer = None

        if rank == 0:
            total_size = sum(counts)
            gathered_timer = np.empty(total_size, dtype=np.float64)
            displacements = np.zeros(size, dtype=int)
            np.cumsum(counts[:-1],out=displacements[1:])
        
        
        print(timer)
        print(gathered_timer,counts,displacements,MPI.DOUBLE)
        comm.Gatherv(timer,[gathered_timer,counts,displacements,MPI.DOUBLE], root=0)
        if rank == 0:
            print("P:",rank,":",gathered_timer)

        comm.Barrier()

        #gather the ants so we can update probability
        # Allgather the ants list from each process
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
        
            # Initialize an empty dictionary to store the unique routes and their corresponding elements
            unique_routes = {}

            for route, count, score in zip(all_ants[0], all_ants[1], all_ants[2]):
                if tuple(route) in unique_routes:
                    unique_routes[tuple(route)] = (
                        unique_routes[tuple(route)][0] + count,
                        max(unique_routes[tuple(route)][1], score),
                    )
                else:
                    unique_routes[tuple(route)] = (count, score)

            # Convert the updated dictionary back to a list
            updated_gathered_ants = [
                [list(route) for route in unique_routes],
                [count for count, _ in unique_routes.values()],
                [score for _, score in unique_routes.values()],
            ]

            # Update the gathered_ants list
            all_ants = updated_gathered_ants
            
            print(len(all_ants[0]))
            
        comm.Barrier()
        
        timeout_buffer = np.empty(1, dtype=int)
        
        if rank == 0:   
            timeout = 0
            for i in range(len(gathered_timer)):
                timeout += all_ants[1][i] * gathered_timer[i]
            timeout = int(timeout / int(nb_ant)) + 1
            timeout_buffer[0] = timeout     
        
        # Broadcast the timeout value from the root process
        comm.Bcast(timeout_buffer, root=0)

        # Extract the timeout value in all processes
        timeout = timeout_buffer[0]

        # Print the timeout value to check if it has been correctly broadcasted
        print("Rank", rank, "received timeout value:", timeout)
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
            # update the best solution
            if all_ants[2][0] > best[1]:
                best = [all_ants[0][0], all_ants[2][0]]
        
        comm.Barrier()
        
        dico = comm.bcast(dico, root=0)
        worst = comm.bcast(worst, root=0)
        if rank == 0:
            print(best)
        
        comm.Barrier()
        
