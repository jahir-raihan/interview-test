from main_file import *


def tsp_brute_force(graph, s):
    # store all vertex apart from source vertex

    vertex = []
    for i in range(1, 10):
        vertex.append(i)

    # store minimum distance

    min_path = maxsize
    next_permutation = permutations(vertex)
    route = ['Uttara Branch']
    path_indexes = None
    for i in next_permutation:

        # store current Path weight(cost)
        current_pathweight = 0

        # compute current path weight
        k = s
        for j in i:
            current_pathweight += graph[k][j]
            k = j
        current_pathweight += graph[k][s]

        # update minimum
        if current_pathweight < min_path:
            min_path = current_pathweight
            path_indexes = list(i)

    for p in path_indexes:
        route.append(branch_names[p])

    return min_path, route


s = 0
result = tsp_brute_force(g, s)  # Here g is imported from main_file.py which is a cost graph.
print("Distance is : ", result[0])
print("Route is : ", ' >>> '.join(result[1]))