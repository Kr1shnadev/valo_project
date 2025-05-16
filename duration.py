import keyboard
import time

tracking = False
key_press_times = {}
press_log = []
q_pressed_once = False
last_action_time = None
last_key_down = None

key_action_map = {
    'w': 'MOVE_FORWARD',
    'a': 'MOVE_LEFT',
    's': 'MOVE_BACK',       # Changed from MOVE_BACKWARD
    'd': 'MOVE_RIGHT'
}


def toggle_tracking():
    global tracking, q_pressed_once
    if not q_pressed_once:
        q_pressed_once = True
        tracking = True
        print("Tracking started. Use W, A, S, D keys to move...")
    else:
        tracking = False
        print("\nTracking stopped. Here's your movement script:\n")
        for action, duration in press_log:
            print(f"{action} {round(duration, 2)}")
        print("\nProgram exited.")
        exit()

def record_key_press():
    global last_action_time, last_key_down

    while True:
        current_time = time.time()
        any_key_pressed = False

        if tracking:
            for key in ['w', 'a', 's', 'd']:
                if keyboard.is_pressed(key):
                    any_key_pressed = True
                    if key not in key_press_times:
                        key_press_times[key] = current_time
                        last_key_down = key
                elif key in key_press_times:
                    duration = current_time - key_press_times[key]
                    action = key_action_map[key]
                    press_log.append((action, duration))
                    last_action_time = current_time
                    del key_press_times[key]

            # Record HOLD if idle for > 0.3 sec
            if not any_key_pressed:
                if last_action_time is not None and current_time - last_action_time > 0.3:
                    press_log.append(("HOLD", current_time - last_action_time))
                    last_action_time = current_time

        if keyboard.is_pressed('q'):
            toggle_tracking()
            time.sleep(0.5)  # debounce

        time.sleep(0.01)

print("Press 'Q' to start tracking. Press 'Q' again to stop and exit.")
record_key_press()
