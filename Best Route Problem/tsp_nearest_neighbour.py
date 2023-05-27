from main_file import *


# Nearest Neighbour Method
def nearest_neighbor(cities, distances):

    route = [cities[0]]
    remaining_cities = cities[1:]

    while remaining_cities:
        closest_city = min(remaining_cities, key=lambda x: distances[route[-1]][x])
        route.append(closest_city)
        remaining_cities.remove(closest_city)

    route.append(route[0])

    dist = 0
    for d in range(len(route) - 1):
        dist += distances[route[d]][route[d+1]]

    return route, dist


route, distance = nearest_neighbor(branch_names, dis)
print("Distance is: ", distance)
print("Route is :", ' >>> '.join(route[:-1]))
