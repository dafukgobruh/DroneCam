import pygame
import numpy as np
import random
from config import (
    CELL_SIZE,
    MARGIN,
    WINDOW_PADDING,
    BAR_HEIGHT,
    BAR_PADDING,
    COLORS,
    DRONE_COLOR,
    ENERGY_BG,
    ENERGY_FG,
    SIM_FPS
)

class GridMap:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.full((rows, cols), ' ', dtype=str)
        self.start = None
        self.goal = None

    def toggle_obstacle(self, r, c):
        if self.grid[r, c] == 'X':
            self.grid[r, c] = ' '
        elif self.grid[r, c] == ' ':
            self.grid[r, c] = 'X'
    
    def toggle_soft_obstacle(self, r, c):
        if self.grid[r, c] == '4':
            self.grid[r, c] = ' '
        elif self.grid[r, c] == ' ':
            self.grid[r, c] = '4'

    def toggle_charger(self, r, c):
        if self.grid[r, c] == 'C':
            self.grid[r, c] = ' '
        elif self.grid[r, c] == ' ':
            self.grid[r, c] = 'C'

    def set_start(self, r, c):
        if self.start:
            self.grid[self.start] = ' '
        self.grid[r, c] = 'S'
        self.start = (r, c)

    def set_goal(self, r, c):
            
        # Nếu goal chưa phải list, khởi tạo thành list
        if not isinstance(self.goal, list):
            # Xóa các điểm goal cũ trên grid nếu có
            if self.goal is not None:
                if isinstance(self.goal, tuple):
                    self.grid[self.goal] = ' '
            self.goal = []

        # Nếu vị trí này chưa là goal, thêm
        if (r, c) not in self.goal:
            self.goal.append((r, c))
            self.grid[r, c] = 'G'
            

    def reset(self):
        self.grid[:, :] = ' '
        self.start = None
        self.goal = None

    def draw(self, screen, heuristic_func=None, goal=None, offset_y=0):
        font = pygame.font.SysFont(None, 18)
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r, c]
                color = COLORS.get(cell, (255,255,255))
                rect = [
                    WINDOW_PADDING + c*(CELL_SIZE+MARGIN) + MARGIN,
                    WINDOW_PADDING + offset_y + r*(CELL_SIZE+MARGIN) + MARGIN,
                    CELL_SIZE,
                    CELL_SIZE
                ]
                pygame.draw.rect(screen, color, rect, border_radius=4)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1, border_radius=4)
                if cell in ['S', 'G', 'C']:
                    label_font = pygame.font.SysFont("consolas", 16, bold=True)
                    label_text = label_font.render(cell, True, (0, 0, 0))
                    label_rect = label_text.get_rect(center=(rect[0] + CELL_SIZE // 2, rect[1] + CELL_SIZE // 2))
                    screen.blit(label_text, label_rect)

                if heuristic_func and goal and cell != 'X':
                    if isinstance(goal, (list, tuple)) and len(goal) > 0 and isinstance(goal[0], tuple):
                        # goal là list các điểm
                        h_val = min(heuristic_func((r, c), g) for g in goal)
                    else:
                        # goal là một điểm đơn
                        h_val = heuristic_func((r, c), goal)
                    h_font = pygame.font.SysFont("consolas", 12)
                    h_text = h_font.render(str(int(h_val)), True, (50, 50, 50))
                    screen.blit(h_text, (rect[0] + 3, rect[1] + 2))  # góc trái trên


def draw_energy_bar(screen, energy, max_energy, width):
       # Thanh nền (bo góc nhẹ)
    pygame.draw.rect(
        screen,
        ENERGY_BG,
        [
            WINDOW_PADDING,
            WINDOW_PADDING - BAR_HEIGHT - BAR_PADDING,
            width,
            BAR_HEIGHT
        ],
        border_radius=8
    )

    # Thanh pin thực tế (màu xanh, bo góc)
    fill_w = int(width * (energy / max_energy))
    pygame.draw.rect(
        screen,
        ENERGY_FG,
        [
            WINDOW_PADDING,
            WINDOW_PADDING - BAR_HEIGHT - BAR_PADDING,
            fill_w,
            BAR_HEIGHT
        ],
        border_radius=8
    )

    font = pygame.font.SysFont("segoeui", 22, bold=True)
    # Hiển thị chữ pin với viền nổi bật
    pin_text = f"{energy}/{max_energy}"
    text_surface = font.render(pin_text, True, (255, 255, 255))
    text_outline = font.render(pin_text, True, (0, 0, 0))  # viền

    # Vẽ viền đen trước (tạo hiệu ứng nổi)
    screen.blit(text_outline, (WINDOW_PADDING + 13, WINDOW_PADDING - BAR_HEIGHT - BAR_PADDING + 4))
    # Vẽ chữ chính màu trắng đè lên
    screen.blit(text_surface, (WINDOW_PADDING + 12, WINDOW_PADDING - BAR_HEIGHT - BAR_PADDING + 3))





def choose_heuristic():
    import pygame
    pygame.init()
    W, H = 500, 360
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Choose Heuristic")

    font_title = pygame.font.SysFont("segoeui", 26, bold=True)
    font_item = pygame.font.SysFont("consolas", 22)
    heuristics = ["manhattan", "euclid", "chebyshev"]
    selected = None
    hover_index = None

    item_rects = []
    running = True

    while running:
        screen.fill((245, 245, 245))
        item_rects = []

        # Vẽ tiêu đề
        title_text = "Click or press 1, 2, 3 to select heuristic"
        title = font_title.render(title_text, True, (20, 20, 20))
        screen.blit(title, ((W - title.get_width()) // 2, 30))

        # Vẽ danh sách lựa chọn
        for i, name in enumerate(heuristics):
            x, y, w, h = 80, 90 + i * 55, 340, 45
            rect = pygame.Rect(x, y, w, h)
            item_rects.append(rect)

            # Highlight nếu được chọn hoặc hover
            if i == selected:
                pygame.draw.rect(screen, (255, 200, 200), rect, border_radius=10)
            elif i == hover_index:
                pygame.draw.rect(screen, (220, 220, 220), rect, border_radius=10)

            color = (255, 0, 0) if i == selected else (0, 0, 0)
            text = font_item.render(f"{i+1}. {name}", True, color)
            screen.blit(text, (x + 20, y + 10))

        pygame.display.flip()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEMOTION:
                hover_index = None
                for i, rect in enumerate(item_rects):
                    if rect.collidepoint(event.pos):
                        hover_index = i
                        break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and hover_index is not None:
                    return heuristics[hover_index]

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_KP1):
                    return heuristics[0]
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    return heuristics[1]
                elif event.key in (pygame.K_3, pygame.K_KP3):
                    return heuristics[2]
                



def run_gui(rows, cols):
    heuristic = choose_heuristic()
    pygame.init()
    SIDEBAR_WIDTH = 360  # khung hướng dẫn bên phải
    screen_w = cols * (CELL_SIZE + MARGIN) + 2 * WINDOW_PADDING + SIDEBAR_WIDTH
    screen_h = rows*(CELL_SIZE+MARGIN) + 2*WINDOW_PADDING
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Dronecam - Map Editor & Simulator")

    gmap = GridMap(rows, cols)
    clock = pygame.time.Clock()
    editing = True

    font = pygame.font.SysFont(None, 24)
    
    while editing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                editing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    editing = False
                elif event.key == pygame.K_r:
                    gmap.reset()
                elif event.key == pygame.K_1:
                    heuristic = "manhattan"
                elif event.key == pygame.K_2:
                    heuristic = "euclidean"
                elif event.key == pygame.K_3:
                    heuristic = "chebyshev"
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                c = (x - WINDOW_PADDING) // (CELL_SIZE + MARGIN)
                r = (y - WINDOW_PADDING) // (CELL_SIZE + MARGIN)
                if 0 <= r < rows and 0 <= c < cols:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_SHIFT:
                        gmap.set_start(r, c)
                    elif mods & pygame.KMOD_CTRL :
                        gmap.set_goal(r, c)
                    elif mods & pygame.KMOD_ALT:
                        gmap.toggle_soft_obstacle(r, c)
                    elif mods & pygame.KMOD_META:
                        gmap.toggle_charger(r, c)
                    else:
                        gmap.toggle_obstacle(r, c)

        screen.fill((200,200,200))
        from pathfinder import get_heuristic_func
        heuristic_func = get_heuristic_func(heuristic)
        # Hiển thị lựa chọn heuristic nổi bật
        bar_rect = pygame.Rect(0, 0, screen.get_width(), 40)
        pygame.draw.rect(screen, (30, 60, 90), bar_rect)  # thanh màu xám đậm

        bar_font = pygame.font.SysFont("arial", 20, bold=True)
        
        bar_text = bar_font.render(
            f"Heuristic: 1️ Manhattan | 2️ Euclidean | 3️ Chebyshev   →  Current: {heuristic.upper()}",
            True, (255, 255, 255)
        )
        screen.blit(bar_text, (WINDOW_PADDING, 10))

        gmap.draw(screen, heuristic_func=heuristic_func, goal=gmap.goal)
        
        #text = font.render(f"Press 1: Manhattan | 2: Euclidean | 3: Chebyshev | Current: {heuristic}", True, (0, 0, 0))
        #screen.blit(text, (WINDOW_PADDING, 5))

        legend_font = pygame.font.SysFont("consolas", 18)
        legend_texts = [
            "SHIFT + Click: Start (S)",
            "CTRL + Click: Goal (G)",
            "Click: Obstacle (X)",
            "ALT + Click: Soft Obstacle (4~6)",
            "META + Click: Charger (C)",
            "R: Reset",
            "Enter: Simulate",
        ]

        sidebar_x = screen.get_width() - SIDEBAR_WIDTH + 10
        sidebar_y = WINDOW_PADDING

        for i, line in enumerate(legend_texts):
            txt = legend_font.render(line, True, (30, 30, 30))
            screen.blit(txt, (sidebar_x, sidebar_y + i*30))



        pygame.display.flip()
        clock.tick(SIM_FPS)

    pygame.quit()
    return gmap.grid, gmap.start, gmap.goal, heuristic

def input_energy(screen, font, default_value=30):
    import pygame
    center_x = screen.get_width() // 2
    input_box = pygame.Rect(0, 0, 200, 40)
    input_box.center = (center_x, screen.get_height() // 2 + 20)

    button_width = 100
    button_height = 35
    button_box = pygame.Rect(0, 0, button_width, button_height)
    button_box.center = (center_x, input_box.y + 80)

    color_active = pygame.Color('lightskyblue3')
    color_border = pygame.Color('gray25')
    color_bg = pygame.Color('white')
    color_btn = pygame.Color('dodgerblue')
    color_btn_hover = pygame.Color('deepskyblue')

    user_text = ''
    running = True
    big_font = pygame.font.SysFont("arial", 26, bold=True)
    small_font = pygame.font.SysFont("consolas", 22)
    mouse_pos = (0, 0)

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        return int(user_text)
                    except ValueError:
                        return default_value
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.unicode.isdigit():
                    user_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_box.collidepoint(event.pos):
                    try:
                        return int(user_text)
                    except ValueError:
                        return default_value

        # Giao diện
        screen.fill((230, 230, 230))

        # Hướng dẫn
        prompt = big_font.render("Enter battery capacity (energy):", True, (10, 10, 10))
        prompt_y = input_box.y - 70
        screen.blit(prompt, (center_x - prompt.get_width() // 2, prompt_y))

        # Ô nhập
        pygame.draw.rect(screen, color_bg, input_box)
        pygame.draw.rect(screen, color_border, input_box, 2)

        txt_surface = small_font.render(user_text or str(default_value), True, color_active)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 7))

        # Nút OK
        btn_color = color_btn_hover if button_box.collidepoint(mouse_pos) else color_btn
        pygame.draw.rect(screen, btn_color, button_box, border_radius=6)
        ok_text = small_font.render("OK", True, (255, 255, 255))
        ok_rect = ok_text.get_rect(center=button_box.center)
        screen.blit(ok_text, ok_rect)

        pygame.display.flip()



from pathfinder import get_heuristic_func

def run_simulation(grid, path, visited, max_energy, heuristic_name='manhattan'):
    heuristic_func = get_heuristic_func(heuristic_name)
    goal_pos = None
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r, c] == 'G':
                goal_pos = (r, c)
                break
    rows, cols = grid.shape
    pygame.init()
    screen_w = cols*(CELL_SIZE+MARGIN) + 2*WINDOW_PADDING
    screen_h = rows*(CELL_SIZE+MARGIN) + 2*WINDOW_PADDING + BAR_HEIGHT + BAR_PADDING
    screen = pygame.display.set_mode((screen_w, screen_h))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    step = 0
    running = True
    log_text = ""  # chuỗi hiện tại để hiển thị log

    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                if step < len(visited):
                    r, c, energy, step_cost, base, delta = visited[step]
                    step += 1
                    log_text = f"Step {step}: Pos=({r},{c}) | Cost={base} + Δ{delta} = {step_cost} | Remaining: {energy}"


        # VẼ TOÀN BỘ KHUNG
        screen.fill((200,200,200))

        # Vẽ bản đồ
        for r in range(rows):
            for c in range(cols):
                cell = grid[r, c]
                color = COLORS.get(cell, (255,255,255))
                pygame.draw.rect(
                    screen,
                    color,
                    [
                        WINDOW_PADDING + c*(CELL_SIZE+MARGIN) + MARGIN,
                        WINDOW_PADDING + BAR_HEIGHT + BAR_PADDING + r*(CELL_SIZE+MARGIN) + MARGIN,
                        CELL_SIZE,
                        CELL_SIZE
                    ],
                    border_radius=6  # bo góc nhẹ
                )


        # Vẽ đường đi (chỉ nếu là ô trống)
        for i in range(step):
            r, c, *_ = visited[i]
            if grid[r, c] == ' ':
                pygame.draw.rect(
                    screen,
                    COLORS['*'],
                    [
                        WINDOW_PADDING + c*(CELL_SIZE+MARGIN) + MARGIN,
                        WINDOW_PADDING + BAR_HEIGHT + BAR_PADDING + r*(CELL_SIZE+MARGIN) + MARGIN,
                        CELL_SIZE,
                        CELL_SIZE
                    ],
                    border_radius=6
                )

        # Vẽ drone nếu đã đi ít nhất 1 bước
        if step > 0:
            r, c, energy, *_ = visited[step - 1]
            pygame.draw.rect(
                screen,
                DRONE_COLOR,
                [
                    WINDOW_PADDING + c*(CELL_SIZE+MARGIN) + MARGIN,
                    WINDOW_PADDING + BAR_HEIGHT + BAR_PADDING + r*(CELL_SIZE+MARGIN) + MARGIN,
                    CELL_SIZE,
                    CELL_SIZE
                ],
                border_radius=6
            )
            if goal_pos and grid[r, c] != 'X':
                h_val = heuristic_func((r, c), goal_pos)
                text = font.render(str(int(h_val)), True, (50, 50, 50))
                screen.blit(text, (
                    WINDOW_PADDING + c*(CELL_SIZE+MARGIN) + MARGIN + 3,
                    WINDOW_PADDING + BAR_HEIGHT + BAR_PADDING + r*(CELL_SIZE+MARGIN) + MARGIN + 3
            ))
            draw_energy_bar(screen, energy, max_energy, cols*(CELL_SIZE+MARGIN))

        # Hiện thông tin pin + log bên dưới
        if log_text:
            log_surface = font.render(log_text, True, (0, 0, 0))
            screen.blit(log_surface, (WINDOW_PADDING, screen_h - 30))

        pygame.display.flip()
        clock.tick(30) 


    pygame.quit()