"""
Rover interface — talks to the Arduino Mega over USB serial.
Background thread polls GPS continuously so the UI always has
a fresh reading without blocking button clicks elsewhere in the
app. Motor commands are sent directly (not polled).
"""

import serial
import threading
import time

MEGA_PORT = "/dev/ttyMega"
MEGA_BAUD = 115200
GPS_POLL_INTERVAL = 1.0  # seconds

_ser = None
_ser_lock = threading.Lock()

_gps_lock = threading.Lock()
_latest_gps = {"fix": False, "lat": None, "lng": None, "sat": 0}

_running = False
_thread = None


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


def _parse_gps_line(line: str):
    # "GPS FIX 16.925519,74.289390 SAT=7"  or  "GPS NOFIX"
    if line.startswith("GPS FIX"):
        try:
            parts = line.split()
            lat_str, lng_str = parts[2].split(",")
            sat = int(parts[3].split("=")[1])
            return {"fix": True, "lat": float(lat_str), "lng": float(lng_str), "sat": sat}
        except (IndexError, ValueError):
            return {"fix": False, "lat": None, "lng": None, "sat": 0}
    return {"fix": False, "lat": None, "lng": None, "sat": 0}


def _poll_loop():
    global _latest_gps, _running
    while _running:
        try:
            line = _send_command("GET_GPS")
            parsed = _parse_gps_line(line)
            with _gps_lock:
                _latest_gps = parsed
        except (serial.SerialException, OSError) as e:
            print(f"rover_control: serial error — {e}")
            time.sleep(2)
        time.sleep(GPS_POLL_INTERVAL)


def start_gps_polling():
    global _running, _thread
    if _running:
        return
    _running = True
    _thread = threading.Thread(target=_poll_loop, daemon=True)
    _thread.start()


def stop_gps_polling():
    global _running
    _running = False


def get_latest_gps():
    with _gps_lock:
        return dict(_latest_gps)


# ---- Motor control (direct, not polled) ----

def set_motor(side: str, value: int):
    return _send_command(f"SET_MOTOR {side} {value}")


def stop_motor(side: str):
    return _send_command(f"STOP_MOTOR {side}")


def stop_rover():
    return _send_command("STOP_ALL")


def get_encoders():
    line = _send_command("GET_ENCODERS")
    # "ENC L=1523 R=1489"
    try:
        parts = line.replace("ENC", "").strip().split()
        left = int(parts[0].split("=")[1])
        right = int(parts[1].split("=")[1])
        return {"left": left, "right": right}
    except (IndexError, ValueError):
        return {"left": None, "right": None}

ROVER_SPEED = 150  # 0-255, tune to taste

def rover_forward():
    set_motor("L", ROVER_SPEED)
    set_motor("R", ROVER_SPEED)

def rover_backward():
    set_motor("L", -ROVER_SPEED)
    set_motor("R", -ROVER_SPEED)

def rover_turn_left():
    set_motor("L", -ROVER_SPEED)
    set_motor("R", ROVER_SPEED)

def rover_turn_right():
    set_motor("L", ROVER_SPEED)
    set_motor("R", -ROVER_SPEED)