# Kích thước bản đồ (mặc định, có thể ghi đè qua GUI)
ROWS = 10
COLS = 15

# Pin tối đa của drone
PIN_MAX_DEFAULT = 30

# Khoảng ngẫu nhiên lệch phí thực tế so với ước lượng (±1)
DELTA_OPTIONS = (-1, 0, 1)

# Tốc độ render trong simulation (frame per second)
SIM_FPS = 5

# Cấu hình GUI
CELL_SIZE = 40
MARGIN = 2
WINDOW_PADDING = 50
BAR_HEIGHT = 20
BAR_PADDING = 10

# Các chế độ chọn ô
MODE_START = 0
MODE_GOAL = 1
MODE_OBSTACLE = 2
MODE_CHARGER = 3

# Trạng thái khởi động lại ma trận
RESET_TRIGGERED = False

# Màu sắc cho GUI
COLORS = {
    ' ': (255, 255, 255),     # Trắng - ô trống
    'X': (0, 0, 0),           # Đen - vật cản
    'C': (0, 255, 0),         # Xanh lá - trạm sạc
    '4': (255, 255, 0),       # Vàng - vật cản mềm
    'S': (0, 0, 255),         # Xanh dương - điểm Start
    'G': (255, 0, 255),       # Hồng - điểm Goal
    '*': (0, 255, 255),       # Cyan - đường đi
}

DRONE_COLOR = (255, 165, 0)     # Cam
ENERGY_BG   = (50,  50,  50)    # Nền thanh pin: xám đậm
ENERGY_FG   = (0,  255,  0)     # Màu thanh pin: xanh lá


SIM_FPS = 15  