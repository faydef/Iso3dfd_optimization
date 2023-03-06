from tree_graph_ant_colony import exploration
from tree_graph_generation import tree_generation

tree_graph, list_dict_parameters = tree_generation(["O3", "O2", "Ofast"], [
    "avx512", "avx2"], 32, 1024, 256, 256)
print(exploration(tree_graph, 100, list_dict_parameters))
