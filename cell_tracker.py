import cv2
import numpy as np
import mss

# Load grid
grid = np.loadtxt("matrix_ascent50.txt", dtype=int)
GRID_SIZE = grid.shape[0]

# Define screen region
region = {'top': 17, 'left': 11, 'width': 500, 'height': 483}
cell_width = region['width'] / GRID_SIZE
cell_height = region['height'] / GRID_SIZE

# Load template
template = cv2.imread("images/neon3.png", 0)
template_h, template_w = template.shape

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
            print(f"Player at: ({row}, {col})")
        else:
            print("Player not detected")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
