import sys
from pathlib import Path
import streamlit as st

# Đảm bảo đường dẫn gốc cho các import trong src
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.ui.theme import inject_theme_system
from src.ui.tab_puzzle import render_tab_puzzle

# 1. Cấu hình trang (Pure Streamlit API)
st.set_page_config(
    page_title="15-Puzzle Game",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Khởi tạo hệ thống Theme và nút Toggle Circular Reveal
inject_theme_system()

# 3. Tiêu đề ứng dụng
st.title("🧩 :rainbow[15-Puzzle Game]")

# 4. Hiển thị giao diện chính của 15-Puzzle
render_tab_puzzle()
