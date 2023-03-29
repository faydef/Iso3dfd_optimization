import random
import math
import sys
import time
from exec_algo import command, execute, execute_nrj, command_nrj, mixed
from representation import initiate

speed = ["O2", "O3", "Ofast"]
avx = ["avx", "avx2", "avx512"]
# Define the objective function to optimize


def objective_function(path, problem, timeout, alpha):
    return mixed(
            {
                "filename": "../iso3dfd-st7/compiled/bin_"
                + speed[path[0]]
                + "_"
                + avx[path[1]]
                + ".exe",
                "size1": str(problem[0]),
                "size2": str(problem[1]),
                "size3": str(problem[2]),
                "num_thread": str(path[2]),
                "dim1": str(path[3]),
                "dim2": str(path[4]),
                "dim3": str(path[5]),
            },
        timeout,
        alpha,
    )


# Define the Particle class
class Particle:
    def __init__(self, bounds, c1, c2, w, problem, timeout, alpha):
        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.position = []
        self.velocity = []
        self.best_position = []
        self.fitness = -1
        self.best_fitness = -1
        self.problem = problem
        self.timeout = timeout
        self.alpha = alpha

        for i in range(len(bounds)):
            if i != 3:
                self.position.append(random.randint(bounds[i][0], bounds[i][1]))
            else:
                self.position.append(
                    (random.randint(bounds[i][0], bounds[i][1]) // 16) * 16
                )
            self.velocity.append(random.uniform(-1, 1))

    def evaluate(self, objective_function):
        start = time.time()
        self.fitness = objective_function(self.position, self.problem, self.timeout, self.alpha)
        end = time.time()

        self.timeout = int(end - start) + 1

        if self.fitness > self.best_fitness or self.best_fitness == -1:
            self.best_position = self.position
            self.best_fitness = self.fitness

    def update_velocity(self, global_best_position):
        for i in range(len(self.position)):
            r1 = random.random()
            r2 = random.random()

            cognitive_velocity = (
                self.c1 * r1 * (self.best_position[i] - self.position[i])
            )
            social_velocity = (
                self.c2 * r2 * (global_best_position[i] - self.position[i])
            )
            self.velocity[i] = (
                self.w * self.velocity[i] + cognitive_velocity + social_velocity
            )

    def update_position(self, bounds):
        for i in range(len(self.position)):
            if i != 3:
                self.position[i] = round(self.position[i] + self.velocity[i])
            else:
                self.position[i] = (
                    round(self.position[i] + self.velocity[i]) // 16
                ) * 16
            if self.position[i] < bounds[i][0]:
                self.position[i] = bounds[i][0]
            elif self.position[i] > bounds[i][1]:
                self.position[i] = bounds[i][1]


# Define the ParticleSwarmOptimization class
class ParticleSwarmOptimization:
    def __init__(
        self,
        objective_function,
        bounds,
        num_particles,
        max_iterations,
        c1,
        c2,
        w,
        problem,
        timeout,
        alpha,
    ):
        self.objective_function = objective_function
        self.bounds = bounds
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.global_best_position = []
        self.global_best_fitness = -1
        self.swarm = []
        self.timeout_global = timeout
        self.alpha = alpha

        for i in range(num_particles):
            self.swarm.append(Particle(bounds, c1, c2, w, problem, timeout, alpha))

    def optimize(self):
        for i in range(self.max_iterations):
            for j in range(self.num_particles):
                self.swarm[j].evaluate(self.objective_function)

                if (
                    self.swarm[j].fitness > self.global_best_fitness
                    or self.global_best_fitness == -1
                ):
                    self.global_best_position = self.swarm[j].position
                    self.global_best_fitness = self.swarm[j].fitness

                if (
                    self.swarm[j].timeout < self.timeout_global
                    or self.timeout_global == -1
                ):
                    self.timeout_global = self.swarm[j].timeout

            for j in range(self.num_particles):
                self.swarm[j].update_velocity(self.global_best_position)
                self.swarm[j].update_position(self.bounds)
                self.swarm[j].timeout = self.timeout_global

            print(
                [
                    speed[self.global_best_position[0]],
                    avx[self.global_best_position[1]],
                    self.global_best_position[2],
                    self.global_best_position[3],
                    self.global_best_position[4],
                ],
                self.global_best_fitness,
            )

        return (self.global_best_position, self.global_best_fitness)


# Example usage:
if __name__ == "__main__":
    (
        num_particles,
        max_iterations,
        problem_1,
        problem_2,
        problem_3,
        timeout,
        c1,
        c2,
        w,
        alpha,
    ) = [int(el) for el in sys.argv[1:-4]] + [float(el) for el in sys.argv[-4:]]
    # Define the boundaries of the search space
    bounds = [(0, 2), (0, 2), (1, 32), (16, problem_1), (1, problem_2), (1, problem_3)]
    optimizer = ParticleSwarmOptimization(
        objective_function,
        bounds,
        num_particles,
        max_iterations,
        c1,
        c2,
        w,
        [problem_1, problem_2, problem_3],
        timeout,
        alpha,
    )
    solution = optimizer.optimize()
    print("Solution: ", solution[0])
    print("Fitness value: ", solution[1])
