"""
Stereo camera capture — background thread continuously grabs
frames from the combined 2560x720 side-by-side USB camera and
splits them into left/right. The UI polls the latest frame via
get_latest_frames() rather than reading the camera directly, so
button clicks elsewhere in the app are never blocked by capture.
"""

import cv2
import threading

CAMERA_INDEX = 0          # /dev/video0
FRAME_WIDTH = 2560
FRAME_HEIGHT = 720

_lock = threading.Lock()
_latest_left = None
_latest_right = None
_running = False
_thread = None


def _capture_loop():
    global _latest_left, _latest_right, _running

    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        print(f"vision: could not open camera index {CAMERA_INDEX}")
        _running = False
        return

    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"vision: camera opened at {actual_w}x{actual_h}")

    while _running:
        ret, frame = cap.read()
        if not ret or frame is None:
            continue

        mid = frame.shape[1] // 2
        left = frame[:, :mid]
        right = frame[:, mid:]

        with _lock:
            _latest_left = left
            _latest_right = right

    cap.release()


def start():
    """Start the background capture thread. Safe to call multiple times."""
    global _running, _thread
    if _running:
        return
    _running = True
    _thread = threading.Thread(target=_capture_loop, daemon=True)
    _thread.start()


def stop():
    global _running
    _running = False


def get_latest_frames():
    """Returns (left_bgr, right_bgr) — either may be None if not ready yet."""
    with _lock:
        return _latest_left, _latest_right