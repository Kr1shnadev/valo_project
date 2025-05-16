from pynput.keyboard import Key, Controller as KeyboardController
import time

keyboard = KeyboardController()

# Key press helper
def press_key(key, duration):
    keyboard.press(key)
    time.sleep(duration)
    keyboard.release(key)

# Action executor
def execute_command(cmd, arg):
    if cmd == "MOVE_FORWARD":
        press_key('w', float(arg))
        print(f"Moving forward for {arg} seconds")
    elif cmd == "MOVE_BACK":
        press_key('s', float(arg))
        print(f"Moving back for {arg} seconds")
    elif cmd == "MOVE_LEFT":
        press_key('a', float(arg))
        print(f"Moving left for {arg} seconds")
    elif cmd == "MOVE_RIGHT":
        press_key('d', float(arg))
        print(f"Moving right for {arg} seconds")
    elif cmd == "HOLD":
        time.sleep(float(arg))
        print(f"Holding for {arg} seconds")
    else:
        print(f"Unknown command: {cmd}")

# Load and run a script
def run_script(filepath):
    print(f"Running script: {filepath}")
    time.sleep(3)  # Time to alt-tab into Valorant
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                cmd, arg = parts
                execute_command(cmd.upper(), arg)
            else:
                print(f"Ignoring invalid line: {line.strip()}")
run_script('map_scripts/ascent_attack.txt')

