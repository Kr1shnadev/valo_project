import cv2

# Load the image
img = cv2.imread('Ascent_minimap.png')  # Replace with your actual minimap image
rows, cols = 40, 40  # Grid size

# Get image dimensions
height, width, _ = img.shape
dy, dx = height // rows, width // cols

# Draw the grid
for y in range(0, height, dy):
    cv2.line(img, (0, y), (width, y), (0, 255, 0), 1)
for x in range(0, width, dx):
    cv2.line(img, (x, 0), (x, height), (0, 255, 0), 1)

cv2.imwrite('grid_overlay.png', img)
