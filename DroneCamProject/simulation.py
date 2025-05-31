# simulation.py
import random
import math
from config import DELTA_OPTIONS


def simulate_traverse(path, cost_map, initial_energy):
    energy = initial_energy
    visited = []
    for idx, (r, c) in enumerate(path):
        base = cost_map[r][c]
        delta = random.choice(DELTA_OPTIONS)
        step_cost = max(1, int(base) + delta)
        if step_cost > energy:
            return visited, False, idx
        energy -= step_cost
        visited.append((r, c, energy))
    return visited, True, len(path)

