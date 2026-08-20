"""
Stereo camera capture + live depth map.

Two independent background threads:
- capture thread: grabs the raw combined 2560x720 frame and splits
  left/right, as fast as the camera/USB allows.
- depth thread: computes a downscaled SGBM disparity map at a
  throttled rate, since this is the expensive part and shouldn't
  compete with raw frame capture or arm-control responsiveness.

Both are started/stopped by the UI page that needs them (see
ui.py) rather than running continuously, to avoid burning CPU
when the camera page isn't even open.
"""

import cv2
import threading
import time

CAMERA_INDEX = 0
FRAME_WIDTH = 2560
FRAME_HEIGHT = 720

DEPTH_SCALE = 0.5       # compute disparity at half resolution — the
                         # main lever for cutting CPU load
DEPTH_INTERVAL = 0.2    # seconds between depth computations (~5 fps)

# ---- capture state ----
_lock = threading.Lock()
_latest_frame = None    # raw 2560x720 stitched BGR frame
_latest_left = None
_latest_right = None
_capture_running = False
_capture_thread = None

# ---- depth state ----
_depth_lock = threading.Lock()
_latest_depth = None
_depth_running = False
_depth_thread = None

_stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=16 * 4,   # multiple of 16; trimmed from 16*5 to cut cost
    blockSize=5,
    P1=8 * 3 * 5 ** 2,
    P2=32 * 3 * 5 ** 2,
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32,
)


def _capture_loop():
    global _latest_frame, _latest_left, _latest_right, _capture_running

    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # minimize internal buffering/latency

    if not cap.isOpened():
        print(f"vision: could not open camera index {CAMERA_INDEX}")
        _capture_running = False
        return

    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"vision: camera opened at {actual_w}x{actual_h}")

    while _capture_running:
        ret, frame = cap.read()
        if not ret or frame is None:
            continue

        mid = frame.shape[1] // 2
        left = frame[:, :mid]
        right = frame[:, mid:]

        with _lock:
            _latest_frame = frame
            _latest_left = left
            _latest_right = right

    cap.release()


def start_capture():
    global _capture_running, _capture_thread
    if _capture_running:
        return
    _capture_running = True
    _capture_thread = threading.Thread(target=_capture_loop, daemon=True)
    _capture_thread.start()


def stop_capture():
    global _capture_running
    _capture_running = False


def get_stitched_frame():
    """Raw combined 2560x720 BGR frame (both sensors, side by side)."""
    with _lock:
        return _latest_frame


def get_latest_frames():
    with _lock:
        return _latest_left, _latest_right


def _depth_loop():
    global _latest_depth, _depth_running

    while _depth_running:
        with _lock:
            left = _latest_left
            right = _latest_right

        if left is None or right is None:
            time.sleep(0.1)
            continue

        small_left = cv2.resize(left, None, fx=DEPTH_SCALE, fy=DEPTH_SCALE)
        small_right = cv2.resize(right, None, fx=DEPTH_SCALE, fy=DEPTH_SCALE)

        gray_left = cv2.cvtColor(small_left, cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(small_right, cv2.COLOR_BGR2GRAY)

        disparity = _stereo.compute(gray_left, gray_right)

        disp_vis = cv2.normalize(
            disparity, None, alpha=0, beta=255,
            norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U
        )
        disp_color = cv2.applyColorMap(disp_vis, cv2.COLORMAP_JET)

        with _depth_lock:
            _latest_depth = disp_color

        time.sleep(DEPTH_INTERVAL)


def start_depth():
    global _depth_running, _depth_thread
    if _depth_running:
        return
    _depth_running = True
    _depth_thread = threading.Thread(target=_depth_loop, daemon=True)
    _depth_thread.start()


def stop_depth():
    global _depth_running
    _depth_running = False


def get_latest_depth():
    with _depth_lock:
        return _latest_depth