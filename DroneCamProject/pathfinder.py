# pathfinder.py (bổ sung hỗ trợ TSP và dùng đúng heuristic cho mọi bước)

import heapq
import math
from itertools import combinations

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def chebyshev(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def get_heuristic_func(name):
    if name == "manhattan":
        return manhattan
    elif name == "euclid":
        return euclidean
    else:
        return chebyshev

def a_star(grid, cost_map, start, goal, heuristic_name):
    rows, cols = len(grid), len(grid[0])
    heuristic_func = get_heuristic_func(heuristic_name)
    open_set = [(heuristic_func(start, goal), 0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_set:
        f, g, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = current[0] + dr, current[1] + dc
                if 0 <= nr < rows and 0 <= nc < cols and cost_map[nr][nc] != math.inf:
                    tentative_g = g + cost_map[nr][nc]
                    if (nr, nc) not in g_score or tentative_g < g_score[(nr, nc)]:
                        g_score[(nr, nc)] = tentative_g
                        f_score = tentative_g + heuristic_func((nr, nc), goal)
                        heapq.heappush(open_set, (f_score, tentative_g, (nr, nc)))
                        came_from[(nr, nc)] = current

    return []

def build_distance_matrix(points, grid, cost_map, heuristic_name):
    dist = {}
    for a, b in combinations(points, 2):
        path = a_star(grid, cost_map, a, b, heuristic_name)
        if not path:
            dist[(a, b)] = dist[(b, a)] = float('inf')
        else:
            dist[(a, b)] = dist[(b, a)] = len(path)
    return dist

def prim_mst(points, dist):
    parent = {p: None for p in points}
    key = {p: float('inf') for p in points}
    key[points[0]] = 0
    visited = set()
    heap = [(0, points[0])]

    while heap:
        _, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        for v in points:
            if v != u and v not in visited and dist[(u, v)] < key[v]:
                key[v] = dist[(u, v)]
                parent[v] = u
                heapq.heappush(heap, (key[v], v))
    return parent

def preorder_traversal(tree, root):
    result = []
    def dfs(u):
        result.append(u)
        for v in tree:
            if tree[v] == u:
                dfs(v)
    dfs(root)
    return result

def tsp_mst_solver(grid, cost_map, start, goals, heuristic_name):
    points = [start] + goals
    dist = build_distance_matrix(points, grid, cost_map, heuristic_name)
    parent = prim_mst(points, dist)
    order = preorder_traversal(parent, start)

    final_path = []
    for i in range(len(order) - 1):
        segment = a_star(grid, cost_map, order[i], order[i + 1], heuristic_name)
        if not segment:
            continue
        if final_path and segment[0] == final_path[-1]:
            final_path.extend(segment[1:])  # loại bỏ lặp
        else:
            final_path.extend(segment)
    return final_path
