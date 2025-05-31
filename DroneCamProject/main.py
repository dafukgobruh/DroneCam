import pygame
from config import ROWS, COLS, PIN_MAX_DEFAULT
from gui import run_gui, run_simulation
from map import build_cost_map
from pathfinder import a_star, tsp_mst_solver
from drone import Drone
from gui import run_gui, run_simulation, input_energy


def main():
    # 1. Chạy GUI để chọn bản đồ và heuristic
    grid, start, goals, heuristic = run_gui(ROWS, COLS)

    # 2. Kiểm tra điểm bắt đầu/kết thúc
    if not start or not goals:
        print("Bạn cần chọn cả điểm bắt đầu và ít nhất một điểm đích trước khi mô phỏng.")
        return

    # 3. Nhập pin bằng giao diện Pygame
    pygame.init()
    screen = pygame.display.set_mode((400, 240))
    font = pygame.font.SysFont(None, 30)
    initial_energy = input_energy(screen, font, default_value=PIN_MAX_DEFAULT)
    pygame.quit()

    # 4. Tạo cost map
    cost_map = build_cost_map(grid)


    destinations = [goals]

    # 6. Chạy mô phỏng
    drone = Drone(grid, cost_map, start, initial_energy, heuristic)
    visited_total = drone.execute_mission(destinations)
    planned_path = [(r, c) for r, c, *_ in visited_total]
    run_simulation(grid, planned_path, visited_total, initial_energy, heuristic)

if __name__ == "__main__":
    main()
