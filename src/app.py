import sys
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.ui.theme import inject_theme_system
from src.ui.tab_puzzle import render_tab_puzzle
from src.ui.tab_benchmark import render_tab_benchmark
from src.ui.tab_leaderboard import render_tab_leaderboard

# 1. Cấu hình trang
st.set_page_config(
    page_title="15-Puzzle Game & AI Solver",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Khởi tạo CSS và Theme tối ưu
inject_theme_system()

# 3. Tiêu đề ứng dụng
st.markdown('<div class="app-title-gradient">🧩 15-Puzzle Game & AI Solver</div>', unsafe_allow_html=True)
st.caption("Ứng dụng trượt ô số 4x4 kinh điển kết hợp AI tối ưu (IDA* vs A*) và Bảng xếp hạng Top 10")

# 4. Hệ thống Tab điều hướng chuyên nghiệp
tab_game, tab_bench, tab_board = st.tabs([
    "🎮 Bàn Cờ & AI Solver",
    "📊 So Sánh Thuật Toán (IDA* vs A*)",
    "🏆 Bảng Xếp Hạng & Lưu Trữ",
])

with tab_game:
    render_tab_puzzle()

with tab_bench:
    render_tab_benchmark()

with tab_board:
    render_tab_leaderboard()
