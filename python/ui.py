"""
Streamlit UI components. Each function renders one control
block and calls into arm_control for the actual hardware action.
"""

from arduino.app_bricks.streamlit_ui import st
import arm_control
import vision

@st.fragment(run_every=0.1)
def vision_panel():
    st.subheader("Camera")
    left, right = vision.get_latest_frames()

    if left is None or right is None:
        st.info("Waiting for camera...")
        return

    c1, c2 = st.columns(2)
    with c1:
        st.image(left, channels="BGR", caption="Left", use_container_width=True)
    with c2:
        st.image(right, channels="BGR", caption="Right", use_container_width=True)

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