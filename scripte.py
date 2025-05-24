from pynput.keyboard import Key, Controller
import time

# Initialize the keyboard controller
keyboard = Controller()

# Dictionary of key and duration (in seconds)
key_sequence = {
    'd': 5.632,
    'w': 3.012,
    'a': 1.303
}

# Function to press and hold a key
def hold_key(key_char, duration):
    print(f"Holding '{key_char}' for {duration:.3f} seconds...")
    keyboard.press(key_char)
    time.sleep(duration)
    keyboard.release(key_char)
    time.sleep(0.1)  # Small delay to ensure key release is registered
    print(f"Released '{key_char}'\n")

time.sleep(1)  # Optional delay before starting the sequence
# Replay the key sequence
for key, duration in key_sequence.items():
    hold_key(key, duration)

print("✅ Key sequence replay completed.")
