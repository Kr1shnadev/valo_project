import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# Load your image
img = plt.imread('Ascent_minimap.png')  # Replace with your actual file name

grid_size = 30
grid = np.ones((grid_size, grid_size), dtype=int)  # Start with all walkable (1)

fig, ax = plt.subplots()
ax.imshow(img)
ax.set_xticks(np.linspace(0, img.shape[1], grid_size+1))
ax.set_yticks(np.linspace(0, img.shape[0], grid_size+1))
ax.grid(color='red', linestyle='-', linewidth=0.5)

# Create a dict to store the patch rectangles
cell_rects = {}

# Draw transparent overlays
def draw_cell_overlay(i, j, state):
    if (i, j) in cell_rects:
        cell_rects[(i, j)].remove()

    cell_width = img.shape[1] / grid_size
    cell_height = img.shape[0] / grid_size
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
    fig.canvas.draw()

def onclick(event):
    if event.xdata is None or event.ydata is None:
        return

    x, y = int(event.xdata), int(event.ydata)
    cell_x = int(x * grid_size / img.shape[1])
    cell_y = int(y * grid_size / img.shape[0])

    # Toggle cell
    grid[cell_y, cell_x] = 0 if grid[cell_y, cell_x] == 1 else 1
    draw_cell_overlay(cell_y, cell_x, grid[cell_y, cell_x])
    print(f"Marked ({cell_y}, {cell_x}) as {'Blocked' if grid[cell_y, cell_x] == 0 else 'Walkable'}")

# Connect the click
fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

# Save when you're done
np.savetxt("grid_matrix.txt", grid, fmt='%d')
