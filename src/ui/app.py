"""
Module điều phối giao diện chính của ứng dụng Streamlit cho 15-Puzzle.
"""
import streamlit as st
from src.ui.tab_puzzle import render_tab_puzzle
from src.ui.theme import inject_theme_system


def main():
    st.set_page_config(
        page_title="15-Puzzle Game",
        page_icon="🧩",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_theme_system()
    st.markdown('<div class="app-title-gradient">🧩 15-Puzzle Game</div>', unsafe_allow_html=True)
    st.caption("Trò chơi trượt ô số 4x4 kinh điển với giải thuật AI thông minh (IDA*) và bảng xếp hạng Top 10")
    render_tab_puzzle()


if __name__ == "__main__":
    main()
