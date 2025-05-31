# map.py
import numpy as np
import math
import random
from config import DELTA_OPTIONS

class GridMap:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.full((rows, cols), ' ', dtype=str)
        self.start = None
        self.goal = None

    def toggle_obstacle(self, row, col):
        if self.grid[row, col] == 'X':
            self.grid[row, col] = ' '
        elif self.grid[row, col] == ' ':
            self.grid[row, col] = 'X'
            
    def toggle_charger(self, row, col):
        if self.grid[row, col] == 'C':
            self.grid[row, col] = ' '
        elif self.grid[row, col] == ' ':
            self.grid[row, col] = 'C'

    def toggle_soft_obstacle(self, row, col):
        if self.grid[row, col] == '4':
            self.grid[row, col] = ' '
        elif self.grid[row, col] == ' ':
            self.grid[row, col] = '4'

    def set_start(self, row, col):
        if self.start:
            self.grid[self.start] = ' '
        self.grid[row, col] = 'S'
        self.start = (row, col)

    def set_goal(self, row, col):
        if not isinstance(self.goal, list):
            if self.goal is not None and isinstance(self.goal, tuple):
                self.grid[self.goal] = ' '
            self.goal = []

        if (row, col) not in self.goal:
            self.goal.append((row, col))
            self.grid[row, col] = 'G'

    def reset(self):
        self.grid[:, :] = ' '
        self.start = None
        self.goal = None


def build_cost_map(grid):
    rows, cols = len(grid), len(grid[0])
    cost_map = [[1 for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            if cell == 'X':  # vật cản tuyệt đối, không đi được
                cost_map[r][c] = math.inf
            elif cell == 'C':  # trạm sạc
                cost_map[r][c] = 1
            elif cell in ('4'):
                cost_map[r][c] = random.randint(4, 6)
            else:
                cost_map[r][c] = random.randint(1, 3)  # chi phí ngẫu nhiên cho ô trống

    return cost_map
