from arduino.app_utils import *
import time

def loop():
    print("Setting X forward...")
    Bridge.call("set_motor_x", 1)
    time.sleep(2)

    print("Stopping X...")
    Bridge.call("set_motor_x", 0)
    time.sleep(1)

    print("Setting X backward...")
    Bridge.call("set_motor_x", -1)
    time.sleep(2)

    print("Stopping X...")
    Bridge.call("set_motor_x", 0)

    state = Bridge.call("get_motor_x")
    print(f"Current direction: {state}")
    time.sleep(3)

App.run(user_loop=loop)