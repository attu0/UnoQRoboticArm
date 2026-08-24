"""
Rover interface — talks to the Arduino Mega over USB serial.

Command protocol (current Mega sketch):
    o <right_pwm> <left_pwm>   — drive both motors (signed, e.g. -150..150)
    e                          — request encoder counts

The Mega has a built-in safety timeout — it auto-stops if it
doesn't receive a fresh "o" command within a short window. So a
single button click alone would only move the rover briefly.
To get continuous movement until Stop is pressed, a background
thread keeps re-sending the current target speed on a steady
interval (faster than the Mega's timeout) until the target is
changed to 0,0.

GPS support removed for now (Mega sketch no longer handles it) —
get_latest_gps() is stubbed to always report no fix so the UI
doesn't break; re-enable once GPS is back on the Mega.
"""

import serial
import threading
import time

MEGA_PORT = "/dev/ttyMega"
MEGA_BAUD = 57600

DRIVE_RESEND_INTERVAL = 0.2  # seconds — must be faster than the
                             # Mega's watchdog timeout

_ser = None
_ser_lock = threading.Lock()

_drive_lock = threading.Lock()
_target_right = 0
_target_left = 0

_drive_thread = None
_drive_thread_started = False


def _get_serial():
    global _ser
    if _ser is None or not _ser.is_open:
        _ser = serial.Serial(MEGA_PORT, MEGA_BAUD, timeout=2)
        time.sleep(2)  # allow Mega to reset after port opens
    return _ser


def _send_command(cmd: str) -> str:
    with _ser_lock:
        ser = _get_serial()
        ser.write((cmd + "\n").encode())
        return ser.readline().decode(errors="ignore").strip()


def _drive_loop():
    while True:
        with _drive_lock:
            right = _target_right
            left = _target_left
        try:
            _send_command(f"o {right} {left}")
        except (serial.SerialException, OSError) as e:
            print(f"rover_control: serial error — {e}")
        time.sleep(DRIVE_RESEND_INTERVAL)


def _ensure_drive_thread():
    global _drive_thread, _drive_thread_started
    if _drive_thread_started:
        return
    _drive_thread_started = True
    _drive_thread = threading.Thread(target=_drive_loop, daemon=True)
    _drive_thread.start()


def set_motors(right: int, left: int):
    """Sets the target drive speed — the background thread keeps
    re-sending this until it's changed again (e.g. by stop_rover)."""
    global _target_right, _target_left
    _ensure_drive_thread()
    with _drive_lock:
        _target_right = right
        _target_left = left


def stop_rover():
    set_motors(0, 0)


def get_encoders():
    """Returns the raw encoder response line. Format from the Mega
    isn't finalized yet — update parsing here once the exact 'e'
    response format is confirmed."""
    return _send_command("e")


ROVER_SPEED = 75  # 0-255, tune to taste


def rover_forward():
    set_motors(ROVER_SPEED, ROVER_SPEED)


def rover_backward():
    set_motors(-ROVER_SPEED, -ROVER_SPEED)


def rover_turn_left():
    set_motors(ROVER_SPEED, -ROVER_SPEED)


def rover_turn_right():
    set_motors(-ROVER_SPEED, ROVER_SPEED)


# ---- GPS (stubbed — Mega sketch doesn't support it right now) ----

def start_gps_polling():
    pass


def stop_gps_polling():
    pass


def get_latest_gps():
    return {"fix": False, "lat": None, "lng": None, "sat": 0}