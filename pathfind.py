import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import heapq
import matplotlib.animation as animation
from matplotlib.widgets import Button

# Load your map and grid
img = plt.imread('images/Ascent_minimap2.png')
grid = np.loadtxt("matrix_ascent60.txt", dtype=int)
grid_size = grid.shape[0]

cell_width = img.shape[1] / grid_size
cell_height = img.shape[0] / grid_size

fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(img)

ax.set_xticks(np.linspace(0, img.shape[1], grid_size + 1))
ax.set_yticks(np.linspace(0, img.shape[0], grid_size + 1))
ax.grid(color='red', linestyle='-', linewidth=0.4)
ax.set_xticklabels([])
ax.set_yticklabels([])

cell_rects = {}
start = None
goal = None
ani = None  # <- Important fix

def draw_cell_overlay(i, j, color, alpha=0.6, radius=0.15):
    if (i, j) in cell_rects:
        cell_rects[(i, j)].remove()
    rect = patches.FancyBboxPatch(
        (j * cell_width, i * cell_height),
        cell_width, cell_height,
        boxstyle="round,pad=0.02,rounding_size={}".format(min(cell_width, cell_height)*radius),
        linewidth=1,
        edgecolor='black',
        facecolor=color,
        alpha=alpha
    )
    ax.add_patch(rect)
    cell_rects[(i, j)] = rect
    fig.canvas.draw_idle()

# Draw blocked cells
for y in range(grid_size):
    for x in range(grid_size):
        if grid[y, x] == 0:
            draw_cell_overlay(y, x, 'darkred', alpha=0.25, radius=0.3)

# Heuristic function
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* Algorithm
def astar(grid, start, goal):
    rows, cols = grid.shape
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
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            neighbor = (current[0] + dy, current[1] + dx)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor] == 0 or neighbor in visited:
                    continue
                tentative_g = cost + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    return None

# Animate the path
def animate_path(path):
    global ani  # <- Prevent GC
    path_cells = path[1:-1]  # exclude start/goal

    def update(frame):
        if frame < len(path_cells):
            i, j = path_cells[frame]
            draw_cell_overlay(i, j, 'gold', alpha=0.75, radius=0.25)

    ani = animation.FuncAnimation(fig, update, frames=len(path_cells), interval=100, repeat=False)
    plt.draw()

# Handle clicks
def onclick(event):
    global start, goal
    if event.xdata is None or event.ydata is None:
        return

    cell_x = int(event.xdata // cell_width)
    cell_y = int(event.ydata // cell_height)

    if not (0 <= cell_x < grid_size and 0 <= cell_y < grid_size):
        return

    if grid[cell_y, cell_x] == 0:
        print("Blocked cell clicked!")
        return

    if start is None:
        start = (cell_y, cell_x)
        draw_cell_overlay(cell_y, cell_x, 'limegreen', alpha=0.9, radius=0.3)
        print(f"Start: {start}")
    elif goal is None:
        goal = (cell_y, cell_x)
        if goal == start:
            print("Goal can't be same as start")
            return
        draw_cell_overlay(cell_y, cell_x, 'deepskyblue', alpha=0.9, radius=0.3)
        print(f"Goal: {goal}")

        path = astar(grid, start, goal)
        if path:
            print(f"Path found. Length: {len(path)}")
            animate_path(path)
        else:
            print("No path found.")
    else:
        print("Reset to select new points.")

# Reset button logic
def reset(event):
    global start, goal, ani
    start = goal = None
    for r in cell_rects.values():
        r.remove()
    cell_rects.clear()
    for y in range(grid_size):
        for x in range(grid_size):
            if grid[y, x] == 0:
                draw_cell_overlay(y, x, 'darkred', alpha=0.25, radius=0.3)
    fig.canvas.draw_idle()
    print("Reset complete.")

# Button widget
ax_reset = plt.axes([0.85, 0.02, 0.1, 0.04])
btn_reset = Button(ax_reset, 'Reset', hovercolor='lightcoral')
btn_reset.on_clicked(reset)

# Bind click
fig.canvas.mpl_connect('button_press_event', onclick)
plt.title("Click: Start (green), Goal (blue), Path animates gold.")
plt.show()
