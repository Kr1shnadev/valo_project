import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# Load image
img = plt.imread('Ascent_minimap.png')

grid_size = 30
grid = np.ones((grid_size, grid_size), dtype=int)  # 1 = walkable, 0 = blocked

fig, ax = plt.subplots()
ax.imshow(img)
ax.set_xticks(np.linspace(0, img.shape[1], grid_size+1))
ax.set_yticks(np.linspace(0, img.shape[0], grid_size+1))
ax.grid(color='red', linestyle='-', linewidth=0.5)

cell_rects = {}

# Calculate dimensions
cell_width = img.shape[1] / grid_size
cell_height = img.shape[0] / grid_size

# Track dragging state
is_dragging = False
drag_mode = None  # "block" or "unblock"
toggled_cells = set()

def draw_cell_overlay(i, j, state):
    if (i, j) in cell_rects:
        cell_rects[(i, j)].remove()

    color = (1, 0, 0, 0.4) if state == 0 else (0, 1, 0, 0.4)  # RGBA

    rect = patches.Rectangle(
        (j * cell_width, i * cell_height),
        cell_width,
        cell_height,
        linewidth=0,
        edgecolor=None,
        facecolor=color
    )
    ax.add_patch(rect)
    cell_rects[(i, j)] = rect
    fig.canvas.draw_idle()

def get_cell(event):
    if event.xdata is None or event.ydata is None:
        return None
    cell_x = int(event.xdata * grid_size / img.shape[1])
    cell_y = int(event.ydata * grid_size / img.shape[0])
    if 0 <= cell_x < grid_size and 0 <= cell_y < grid_size:
        return (cell_y, cell_x)
    return None

def on_press(event):
    global is_dragging, drag_mode, toggled_cells
    cell = get_cell(event)
    if not cell:
        return

    is_dragging = True
    toggled_cells = set()

    y, x = cell
    drag_mode = "block" if grid[y, x] == 1 else "unblock"

    toggle_cell(y, x)

def on_release(event):
    global is_dragging, toggled_cells
    is_dragging = False
    toggled_cells = set()

def on_motion(event):
    if not is_dragging:
        return
    cell = get_cell(event)
    if not cell:
        return
    y, x = cell
    if (y, x) not in toggled_cells:
        toggle_cell(y, x)

def toggle_cell(y, x):
    global toggled_cells
    grid[y, x] = 0 if drag_mode == "block" else 1
    draw_cell_overlay(y, x, grid[y, x])
    toggled_cells.add((y, x))
    print(f"{'Blocked' if grid[y,x]==0 else 'Unblocked'} ({y}, {x})")

# Mouse events
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

plt.show()

# Save
np.savetxt("grid_matrix.txt", grid, fmt='%d')
