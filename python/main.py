import subprocess
import sys

try:
    import serial
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyserial", "--break-system-packages"])
    import serial


from arduino.app_bricks.streamlit_ui import st
from arduino.app_utils import App
import ui

st.set_page_config(page_title="Robotic Arm", layout="centered")
ui.inject_mobile_styles()

pg = st.navigation([
    st.Page(ui.render_arm_page, title="Arm Control", icon="🦾"),
    st.Page(ui.render_camera_page, title="Camera", icon="📷"),
    st.Page(ui.render_rover_page, title="Rover", icon="🛰️"),
])
pg.run()

App.run()