import pyautogui
import cv2
import numpy as np

# Set your minimap region here manually (adjust these!)
minimap_x = 11 
minimap_y = 17    
minimap_width = 500
minimap_height = 483

# Take screenshot of minimap region
screenshot = pyautogui.screenshot(region=(minimap_x, minimap_y, minimap_width, minimap_height))

# Convert screenshot to OpenCV format (RGB to BGR)
minimap_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# Show the image using OpenCV
cv2.imshow("Minimap Capture", minimap_img)
cv2.imwrite("minimap_capture.png", minimap_img)  # Save the image if needed
cv2.waitKey(0)
cv2.destroyAllWindows()
