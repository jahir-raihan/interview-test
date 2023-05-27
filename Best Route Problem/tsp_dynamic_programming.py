from main_file import *

# Dynamic Programming Approach -> It gives the optimal distance but takes either time or space.

# We will use bitmask to track visited cities , It's faster than real values.
# However, I couldn't find a way to track the path in this algorithm, it only produces distance

n = 10  # Count of cities
visited = (1 << n) - 1
dp = [[-1]*n]*(visited+1)   # We know that number of distinct possible combinations is 2^n


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