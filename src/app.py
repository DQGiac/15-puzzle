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

# 3. Hero Header Banner hiện đại
hero_html = """
<div class="hero-header-card">
    <div class="hero-title-area">
        <h1 class="app-title-gradient">🧩 15-Puzzle Game & AI Solver</h1>
        <p class="hero-subtitle">Trò chơi trượt ô số 4×4 kinh điển chuẩn C++ Raylib • Tích hợp AI đối đầu IDA* vs A*</p>
    </div>
    <div class="hero-badges-group">
        <span class="tech-pill accent-blue">⚡ IDA* Heuristic</span>
        <span class="tech-pill accent-purple">🌲 A* MinHeap</span>
        <span class="tech-pill accent-gold">🏆 Top 10 Records</span>
        <span class="tech-pill">🎮 C++ Raylib Engine</span>
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

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
