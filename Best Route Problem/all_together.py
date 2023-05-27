from math import radians, cos, sin, asin, sqrt
from sys import maxsize
from itertools import permutations


def distance(l1, l2, l3, l4):

    # radians which converts from degrees to radians.
    # Haversine formula

    d_lon = radians(l4) - radians(l3)
    d_lat = radians(l2) - radians(l1)
    a = sin(d_lat / 2) ** 2 + cos(l1) * cos(l2) * sin(d_lon / 2) ** 2
    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. We can use 3956 for miles
    r = 6371

    # calculating  the result
    return c * r


lat_longs = [
    [23.8728568, 90.3984184], [23.8513998, 90.3944536], [23.8330429, 90.4092871],
    [23.8679743, 90.3840879], [23.8248293, 90.3551134], [23.827149, 90.4106238],
    [23.8629078, 90.3816318], [23.8673789, 90.429412], [23.8248938, 90.3549467],
    [23.813316, 90.4147498]
]

g = [[0] * 10 for _ in range(10)]  # The distance between two points in form of adjacency matrix

# Loops for calculating distance between two location using their latitude and longitude
for i in range(10):  # 10 -> count of cities
    for j in range(10):  # 10 -> count of cities
        if i != j:
            lat1 = lat_longs[i][0]
            lat2 = lat_longs[j][0]
            lng1 = lat_longs[i][1]
            lng2 = lat_longs[j][1]
            g[i][j] = round(distance(lat1, lat2, lng1, lng2), 2)


# Branch Names

branch_names = ['Uttara Branch', 'City Bank Airport', 'City Bank Nikunja', 'City Bank Beside Uttara Diagnostic',
                'City Bank Mirpur 12', 'City Bank Le Meridien', 'City Bank Shaheed Sarani', 'City Bank Narayanganj',
                'City Bank Pallabi', 'City Bank JFP']

# Adjacency matrix for storing distance between cities -> Only for Nearest Neighbour method.
dis = {}

# Inserting distances to the matrix

for idx in range(10): # We know that the count of branches are 10
    dis[branch_names[idx]] = {}
    for cost_distance in range(10):
        if idx != cost_distance:
            dis[branch_names[idx]][branch_names[cost_distance]] = g[idx][cost_distance]

# Now we got the distances between cities in form of km in matrix "g" and in Adjacency Matrix "dis".


# Brute Force
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


# Dynamic Programming Approach -> It gives the optimal distance but takes either time or space.

# We will use bitmask to track visited cities , It's faster than real values.
# However, I couldn't find a way to track the path in this algorithm

n = 10  # Count of cities
visited = (1 << n) - 1
dp = [[-1]*n]*(visited+1)  # We know that number of distinct possible combinations is 2^n


def tsp(mask, pos):
    if mask == visited:
        return g[pos][0]

    # Lookup case
    if dp[mask][pos] != -1:
        return dp[mask][pos]

    # Loop through unvisited cities
    ans = 10**9

    for city in range(n):

        if mask & (1 << city) == 0:
            new_ans = g[pos][city] + tsp(mask | (1 << city), city)

            if new_ans < ans:
                ans = new_ans

    dp[mask][pos] = ans
    return ans


total_distance = tsp(1, 0)
print('Distance is : ', total_distance)
