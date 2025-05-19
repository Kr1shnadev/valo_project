import cv2
import numpy as np
import mss
import heapq
import pyautogui
import time

# Load grid
grid = np.loadtxt("matrix_ascent.txt", dtype=int)
GRID_SIZE = grid.shape[0]

# Screen capture region (adjust based on your screen resolution and minimap position)
region = {'top': 17, 'left': 11, 'width': 500, 'height': 483}

# Grid cell sizes
cell_width = region['width'] / GRID_SIZE
cell_height = region['height'] / GRID_SIZE

# Load template (player dot)
template = cv2.imread("images/neon_dot.png", 0)
template_h, template_w = template.shape

# Global goal variable
goal = None

# Mouse callback function
def select_goal(event, x, y, flags, param):
    global goal
    if event == cv2.EVENT_LBUTTONDOWN:
        row = int(y / cell_height)
        col = int(x / cell_width)
        goal = (row, col)
        print(f"Goal selected at cell: {goal}")


# ---- A* Pathfinding ----
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid, start, goal):
    open_set = [(0 + heuristic(start, goal), 0, start)]
    came_from = {}
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, cost, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        visited.add(current)
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0]+dy, current[1]+dx)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
                if grid[neighbor] == 0 or neighbor in visited:
                    continue
                tentative_g = cost + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    heapq.heappush(open_set, (tentative_g + heuristic(neighbor, goal), tentative_g, neighbor))
    return None

# ---- Movement Simulation ----
def move_toward(current, next):
    dy = next[0] - current[0]
    dx = next[1] - current[1]

    move_duration = 1  # Smooth timing
    if dy == -1:
        pyautogui.keyDown('w')
        time.sleep(move_duration)
        pyautogui.keyUp('w')
    elif dy == 1:
        pyautogui.keyDown('s')
        time.sleep(move_duration)
        pyautogui.keyUp('s')
    elif dx == -1:
        pyautogui.keyDown('a')
        time.sleep(move_duration)
        pyautogui.keyUp('a')
    elif dx == 1:
        pyautogui.keyDown('d')
        time.sleep(move_duration)
        pyautogui.keyUp('d')

    time.sleep(0.05)  # Cooldown between moves


# ---- Main Loop ----
# Prompt for goal selection
print("Please click on the minimap to select your destination cell...")

# Show frame to select destination
with mss.mss() as sct:
    while goal is None:
        screen = sct.grab(region)
        frame = np.array(screen)
        frame_copy = frame.copy()

        cv2.imshow("Select Destination", frame_copy)
        cv2.setMouseCallback("Select Destination", select_goal)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Selection cancelled.")
            cv2.destroyAllWindows()
            exit()

cv2.destroyAllWindows()
print(f"Destination selected: {goal}")

time.sleep(2)  # Delay to switch to game window
with mss.mss() as sct:
    while True:
        screen = sct.grab(region)
        frame = np.array(screen)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > 0.75:
            top_left = max_loc
            center_x = top_left[0] + template_w // 2
            center_y = top_left[1] + template_h // 2

            row = int(center_y / cell_height)
            col = int(center_x / cell_width)
            current_pos = (row, col)

            print(f"Current: {current_pos}, Goal: {goal}")

            if current_pos == goal:
                print("Reached destination.")
                break

            path = astar(grid, current_pos, goal)
            if path and len(path) > 1:
                next_step = path[1]
                move_toward(current_pos, next_step)
            else:
                print("No path found or already at goal.")
        else:
            print("Player dot not detected.")

        # Optional: visualize detection
        cv2.rectangle(frame, top_left, (top_left[0]+template_w, top_left[1]+template_h), (0,255,0), 2)
        cv2.imshow("Minimap Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()
