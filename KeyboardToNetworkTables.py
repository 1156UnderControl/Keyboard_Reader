import networktables as networkTablesCore
import time
import evdev
from threading import Timer

def main():
    def release_key(key_name: str) -> None:
        print(f"Sending: {key_name} -> {False}")
        table.putBoolean(key_name, False)

    def timed_keypress(key_name: str, press_time: float) -> None:
        print(f"Sending: {key_name} -> {True}")
        table.putBoolean(key_name, True)
        timer = Timer(press_time, release_key, [key_name])
        timer.start()

    # Get all input devices
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    keyboard_device = None

    # Identify the correct keyboard
    for device in devices:
        if "keyboard" in device.name.lower():  # Change this if needed
            keyboard_device = device
            print(f"Using keyboard: {device.name} at {device.path}")
            break

    if not keyboard_device:
        print("No USB keyboard found!")
        return

    networkTables = networkTablesCore.NetworkTablesInstance.getDefault()

    print("Setting up NetworkTables client")
    networkTables.startClient("KeyboardToNT")
    networkTables.setServer("10.11.56.2")
    networkTables.startDSClient()

    print("Waiting for connection to NetworkTables server...")
    while not networkTables.isConnected():
        time.sleep(0.1)

    print("Connected!")
    table = networkTables.getTable("OperatorController")

    # Read from the USB keyboard only
    for event in keyboard_device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            key_name = key_event.keycode.lower()

            if key_event.keystate == evdev.KeyEvent.key_down:
                timed_keypress(key_name, 0.100)

if __name__ == '__main__':
    main()