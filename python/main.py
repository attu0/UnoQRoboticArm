from arduino.app_bricks.streamlit_ui import st
from arduino.app_utils import App
import ui
import vision

st.set_page_config(page_title="Robotic Arm", layout="centered")
ui.inject_mobile_styles()

vision.start()  # begin background camera capture

st.title("🦾 Robotic Arm Control")

ui.axis_controls("x")
st.divider()

ui.axis_controls("y")
st.divider()

ui.joint_za_controls()
st.divider()

ui.servo_controls()
st.divider()

ui.vision_panel()
st.divider()

ui.stop_all_button()

App.run()