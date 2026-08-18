from arduino.app_bricks.streamlit_ui import st
from arduino.app_utils import App, Bridge

st.set_page_config(page_title="Robotic Arm", layout="centered")

# Larger touch-friendly buttons for mobile
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


def set_motor(axis, direction):
    Bridge.call(f"set_motor_{axis}", direction)


def stop_motor(axis):
    Bridge.call(f"stop_motor_{axis}")


def axis_controls(axis, label=None):
    st.subheader(label or f"{axis.upper()} axis")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("↻ CW", key=f"{axis}_cw", use_container_width=True):
            set_motor(axis, 1)
    with c2:
        if st.button("■ Stop", key=f"{axis}_stop", use_container_width=True):
            stop_motor(axis)
    with c3:
        if st.button("↺ CCW", key=f"{axis}_ccw", use_container_width=True):
            set_motor(axis, -1)


def joint_za_controls():
    st.subheader("Z / A Joint")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("↻ CW", key="za_cw", use_container_width=True):
            Bridge.call("set_joint_za", 1)
    with c2:
        if st.button("■ Stop", key="za_stop", use_container_width=True):
            Bridge.call("stop_joint_za")
    with c3:
        if st.button("↺ CCW", key="za_ccw", use_container_width=True):
            Bridge.call("set_joint_za", -1)


def servo_controls():
    st.subheader("Gripper (3s run)")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("↻ CW", key="servo_cw", use_container_width=True):
            Bridge.call("set_servo_dir", 1)
    with c2:
        if st.button("■ Stop", key="servo_stop", use_container_width=True):
            Bridge.call("stop_servo")
    with c3:
        if st.button("↺ CCW", key="servo_ccw", use_container_width=True):
            Bridge.call("set_servo_dir", -1)


st.title("🦾 Robotic Arm Control")

axis_controls("x")
st.divider()

axis_controls("y")
st.divider()

joint_za_controls()
st.divider()

servo_controls()
st.divider()

if st.button("🛑 STOP ALL", type="primary", use_container_width=True):
    Bridge.call("stop_all")

App.run()