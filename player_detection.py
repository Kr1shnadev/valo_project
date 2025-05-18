import cv2
import numpy as np
import mss

# Load dot template in grayscale
template = cv2.imread("cypher_dot2.png", 0)
template_h, template_w = template.shape

# Define minimap capture region (adjust based on your screen)
region = {'top': 17, 'left': 11, 'width': 500, 'height': 483}

# Grid setup
GRID_ROWS, GRID_COLS = 30, 30
cell_width = region['width'] / GRID_COLS
cell_height = region['height'] / GRID_ROWS

with mss.mss() as sct:
    while True:
        # Capture minimap region
        screen = sct.grab(region)
        frame = np.array(screen)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Template matching
        result = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > 0.75:
            top_left = max_loc
            bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

            # Compute center of matched dot
            center_x = top_left[0] + template_w // 2
            center_y = top_left[1] + template_h // 2

            # Map to grid cell (row, col)
            grid_row = int(center_y / cell_height)
            grid_col = int(center_x / cell_width)

            print(f"Player dot at: ({center_x}, {center_y}) → Grid cell: ({grid_row}, {grid_col})")
        else:
            print("Player dot not found")

        # Show detection result
        cv2.imshow("Live Dot Detection", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()
