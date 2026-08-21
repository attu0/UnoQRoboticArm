"""
Streamlit UI components. Each function renders one control
block and calls into arm_control for the actual hardware action.
"""

from arduino.app_bricks.streamlit_ui import st
import arm_control
import vision
import rover_control


def inject_mobile_styles():
    st.markdown("""
    <style>
        div.stButton > button {
            height: 3.2em;
            font-size: 1.1em;
            font-weight: 600;
        }
        div.stButton > button[kind="primary"] {
            height: 3.6em;
            font-size: 1.2em;
        }
    </style>
    """, unsafe_allow_html=True)


def axis_controls(axis: str, label: str = None):
    st.subheader(label or f"{axis.upper()} axis")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("↻ CW", key=f"{axis}_cw", use_container_width=True):
            arm_control.set_motor(axis, 1)
    with c2:
        if st.button("■ Stop", key=f"{axis}_stop", use_container_width=True):
            arm_control.stop_motor(axis)
    with c3:
        if st.button("↺ CCW", key=f"{axis}_ccw", use_container_width=True):
            arm_control.set_motor(axis, -1)


def joint_za_controls():
    st.subheader("Z / A Joint")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("↻ CW", key="za_cw", use_container_width=True):
            arm_control.set_joint_za(1)
    with c2:
        if st.button("■ Stop", key="za_stop", use_container_width=True):
            arm_control.stop_joint_za()
    with c3:
        if st.button("↺ CCW", key="za_ccw", use_container_width=True):
            arm_control.set_joint_za(-1)


def servo_controls():
    st.subheader("Gripper (3s run)")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("↻ CW", key="servo_cw", use_container_width=True):
            arm_control.set_servo_dir(1)
    with c2:
        if st.button("■ Stop", key="servo_stop", use_container_width=True):
            arm_control.stop_servo()
    with c3:
        if st.button("↺ CCW", key="servo_ccw", use_container_width=True):
            arm_control.set_servo_dir(-1)


def stop_all_button():
    if st.button("🛑 STOP ALL", type="primary", use_container_width=True):
        arm_control.stop_all()


# ============================================================
# PAGES
# ============================================================

def render_arm_page():
    # Camera not needed here — stop it to free CPU for arm control
    vision.stop_depth()
    vision.stop_capture()

    st.title("🦾 Robotic Arm Control")

    axis_controls("x")
    st.divider()

    axis_controls("y")
    st.divider()

    joint_za_controls()
    st.divider()

    servo_controls()
    st.divider()

    stop_all_button()


def render_camera_page():
    # Only spin up capture/depth while this page is actually open
    vision.start_capture()
    vision.start_depth()

    st.title("📷 Stereo Camera")

    stitched_panel()
    st.divider()
    depth_panel()


@st.fragment(run_every=0.1)
def stitched_panel():
    st.subheader("Stitched Stereo Feed (2560x720)")
    frame = vision.get_stitched_frame()
    if frame is None:
        st.info("Waiting for camera...")
        return
    st.image(frame, channels="BGR", use_container_width=True)


@st.fragment(run_every=0.3)
def depth_panel():
    st.subheader("Live Depth Map")
    depth = vision.get_latest_depth()
    if depth is None:
        st.info("Computing depth...")
        return
    st.image(depth, channels="BGR", use_container_width=True)

@st.fragment(run_every=1.0)
def rover_gps_panel():
    st.subheader("GPS")
    gps = rover_control.get_latest_gps()

    if gps["fix"]:
        st.success(f"Fix — {gps['sat']} satellites")
        st.metric("Latitude", f"{gps['lat']:.6f}")
        st.metric("Longitude", f"{gps['lng']:.6f}")
        st.map({"lat": [gps["lat"]], "lon": [gps["lng"]]}, zoom=15)
    else:
        st.warning("No fix — waiting for satellites")


def render_rover_page():
    rover_control.start_gps_polling()
    st.title("🛰️ Rover")
    rover_gps_panel()