from arduino.app_bricks.streamlit_ui import st
from arduino.app_utils import App, Bridge


def set_motor(axis, direction):
    Bridge.call(f"set_motor_{axis}", direction)


def stop_motor(axis):
    Bridge.call(f"stop_motor_{axis}")


def axis_controls(axis):
    st.subheader(f"{axis.upper()} axis")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("↻ CW", key=f"{axis}_cw"):
            set_motor(axis, 1)

    with col2:
        if st.button("■ Stop", key=f"{axis}_stop"):
            stop_motor(axis)

    with col3:
        if st.button("↺ CCW", key=f"{axis}_ccw"):
            set_motor(axis, -1)


def servo_controls():
    st.subheader("Servo (Gripper)")
    angle = st.slider("Angle", min_value=0, max_value=180, value=90, key="servo_angle_slider")
    if st.button("Set angle", key="servo_set"):
        Bridge.call("set_servo_angle", angle)


st.title("Robotic Arm Control")

for axis in ["x", "y", "z", "a"]:
    axis_controls(axis)

st.divider()
servo_controls()

st.divider()
if st.button("STOP ALL", type="primary"):
    Bridge.call("stop_all")

App.run()