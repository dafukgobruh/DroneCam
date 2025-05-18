import os
import heapq

def readGraph():
    basePath = os.path.dirname(__file__)
    filePath = os.path.join(basePath, "AStarInput.txt")

    with open(filePath, 'r') as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    graph = [list(map(int, line.strip().split())) for line in lines[1:n+1]]
    heuristic = list(map(int, lines[n+1].strip().split()))  #h(n) line
    start, goal = map(int, lines[-1].strip().split())
    return graph, heuristic, start, goal

def printAnswer(path, cost, graph):
    basePath = os.path.dirname(__file__)
    filePath = os.path.join(basePath, "AStarOutput.txt")

    with open(filePath, 'w') as f:
        for i in range(len(path) - 1):
            f.write(f"{path[i]} - {path[i+1]} : {graph[path[i]][path[i+1]]}\n")
        f.write(f"A* algorithm's cost: {cost}\n")

def aStar(graph, heuristic, start, goal):
    n = len(graph)
    goal = goal if goal is not None else n - 1  #ternary operator
    openSet = [(heuristic[start], 0, start, [start])]  
    visited = [False] * n

    while openSet:
        f, g, u, path = heapq.heappop(openSet)  #find the minimum cost
        if visited[u]:
            continue
        visited[u] = True

        if u == goal:
            return path, g, graph

        for v, weight in enumerate(graph[u]):
            if weight > 0 and not visited[v]:
                heapq.heappush(openSet, (g + weight + heuristic[v], g + weight, v, path + [v]))

    return [], -1, graph

printAnswer(*aStar(*readGraph()))  #run