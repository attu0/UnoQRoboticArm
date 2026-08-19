"""
Hardware interface layer — every call into Bridge lives here.
UI code should never call Bridge directly; it should call these
functions instead, so the mapping to sketch-side function names
only needs to change in one place.
"""

from arduino.app_utils import Bridge


def set_motor(axis: str, direction: int):
    Bridge.call(f"set_motor_{axis}", direction)


def stop_motor(axis: str):
    Bridge.call(f"stop_motor_{axis}")


def set_joint_za(direction: int):
    Bridge.call("set_joint_za", direction)


def stop_joint_za():
    Bridge.call("stop_joint_za")


def set_servo_dir(direction: int):
    Bridge.call("set_servo_dir", direction)


def stop_servo():
    Bridge.call("stop_servo")


def stop_all():
    Bridge.call("stop_all")