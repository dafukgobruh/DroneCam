from pathfinder import a_star, tsp_mst_solver
import random
from config import DELTA_OPTIONS

class Drone:
    def __init__(self, grid, cost_map, start, energy_max, heuristic):
        self.grid = grid
        self.cost_map = cost_map
        self.pos = start
        self.energy = energy_max
        self.max_energy = energy_max
        self.heuristic = heuristic

    def estimate_path_cost(self, path):
        # Ước lượng tổng chi phí path (dựa vào base cost, chưa tính delta)
        if not path:
            return float('inf')
        return sum(max(1, self.cost_map[r][c]) for r, c in path)

    def travel_path(self, path):
        visited = []
        for (r, c) in path:
            base = self.cost_map[r][c]
            delta = random.choice(DELTA_OPTIONS)
            step_cost = max(1, int(base) + delta)
            if step_cost > self.energy:
                return visited, False
            self.energy -= step_cost
            self.pos = (r, c)
            if self.grid[r][c] == 'C':
                self.energy = self.max_energy
            visited.append((r, c, self.energy, step_cost, base, delta))
        return visited, True

    def find_nearest_charger(self):
        rows, cols = len(self.grid), len(self.grid[0])
        candidates = []
        for r in range(rows):
            for c in range(cols):
                if self.grid[r][c] == 'C':
                    pred_path = a_star(self.grid, self.cost_map, self.pos, (r, c), self.heuristic)
                    if not pred_path:
                        continue
                    pred_cost = sum(self.cost_map[x][y] for x, y in pred_path)
                    if pred_cost <= self.energy:
                        margin = self.energy - pred_cost
                        candidates.append(((r, c), pred_cost, margin))
        if not candidates:
            return None
        candidates.sort(key=lambda x: (-x[2], x[1]))
        return candidates[0][0]

    def execute_mission(self, destinations):
        visited_total = []
        safe_factor = 1.1
        max_retries = 10  # giới hạn thử lại

        for dest in destinations:
            retries = 0
            while retries < max_retries:
                if isinstance(dest, (list, tuple)) and len(dest) > 0 and isinstance(dest[0], tuple):
                    pred_path = tsp_mst_solver(self.grid, self.cost_map, self.pos, dest, self.heuristic)
                else:
                    pred_path = a_star(self.grid, self.cost_map, self.pos, dest, self.heuristic)

                if not pred_path:
                    print("⚠️ No path to goal. Drone stays put.")
                    break

                est_cost = self.estimate_path_cost(pred_path)

                if self.energy >= est_cost * safe_factor:
                    visited, reached = self.travel_path(pred_path)
                    visited_total.extend(visited)
                    if reached:
                        break
                    else:
                        print("⚠️ Ran out of energy mid-way. Drone stops.")
                        break

                charger = self.find_nearest_charger()
                if charger:
                    charger_path = a_star(self.grid, self.cost_map, self.pos, charger, self.heuristic)
                    if charger_path:
                        charger_cost = self.estimate_path_cost(charger_path)
                        if charger_cost <= self.energy:
                            visited_c, reached_c = self.travel_path(charger_path)
                            visited_total.extend(visited_c)
                            if reached_c:
                                self.energy = self.max_energy
                                print("✅ Recharged successfully.")
                                retries += 1
                                continue
                            else:
                                print("⚠️ Failed to reach charger. Drone stops.")
                                break

                print("❌ No reachable charger or too far. Drone stays put.")
                break
            else:
                print(f"⚠️ Max retries reached for destination {dest}. Moving on.")

        return visited_total
