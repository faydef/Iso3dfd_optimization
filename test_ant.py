from tree_graph_ant_colony import exploration
from tree_graph_generation import tree_generation

tree_graph = tree_generation(["O3", "O2", "Ofast"], [
                             "avx512", "avx2"], 32, 256, 256, 256)
print(exploration(tree_graph, 100))
