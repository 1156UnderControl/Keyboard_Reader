import networktables as networkTablesCore
import keyboard
import time
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

    def on_action(event: keyboard.KeyboardEvent):
        if (event.name == "/"):
            return
        value = event.event_type == keyboard.KEY_DOWN
        if value:
            key_name = "numpad" + event.name if event.is_keypad else event.name.lower()
            timed_keypress(key_name, 0.100)

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

    keyboard.hook(lambda e: on_action(e))
    keyboard.wait()

if __name__ == '__main__':
    main()