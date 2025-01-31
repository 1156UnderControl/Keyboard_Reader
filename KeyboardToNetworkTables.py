from networktables import pynetworktables as ntcore
import keyboard
import time

def main():
    def on_action(event: keyboard.KeyboardEvent):
        if (event.name == "/"):
            return
        value = event.event_type == keyboard.KEY_DOWN
        key_name = "numpad" + event.name if event.is_keypad else event.name.lower()
        print(f"Sending: {key_name} -> {value}")
        table.putBoolean(key_name, value)

    ntcoreinst = ntcore.NetworkTableInstance.getDefault()

    print("Setting up NetworkTables client")
    ntcoreinst.startClient4("KeyboardToNT")
    ntcoreinst.setServer("10.11.56.2")
    ntcoreinst.startDSClient()

    print("Waiting for connection to NetworkTables server...")
    while not ntcoreinst.isConnected():
        time.sleep(0.1)

    print("Connected!")
    table = ntcoreinst.getTable("SmartDashboard/keyboard")

    keyboard.hook(lambda e: on_action(e))
    keyboard.wait()

if __name__ == '__main__':
    main()