import sys
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
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

# 3. Tiêu đề ứng dụng bão hòa cao, tương phản sắc nét trong cả Light & Dark
st.markdown('<div class="app-title-gradient">🧩 15-Puzzle Game</div>', unsafe_allow_html=True)
st.caption("Trò chơi trượt ô số 4x4 kinh điển với giải thuật AI thông minh (IDA*) và bảng xếp hạng Top 10")

# 4. Hiển thị giao diện chính của 15-Puzzle
render_tab_puzzle()

