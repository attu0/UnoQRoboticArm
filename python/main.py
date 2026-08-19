from arduino.app_bricks.streamlit_ui import st
from arduino.app_utils import App
import python.ui as ui
import python.vision as vision  # noqa: F401 — imported so it's wired in once built out

st.set_page_config(page_title="Robotic Arm", layout="centered")
ui.inject_mobile_styles()

st.title("🦾 Robotic Arm Control")

ui.axis_controls("x")
st.divider()

ui.axis_controls("y")
st.divider()

ui.joint_za_controls()
st.divider()

ui.servo_controls()
st.divider()

# vision.render_vision_panel()  # uncomment once vision.py has content
# st.divider()

ui.stop_all_button()

App.run()