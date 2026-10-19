"""
Module điều phối giao diện chính của ứng dụng Streamlit.

Tác dụng trong dự án:
    - Thiết lập cấu hình trang (tiêu đề, icon, layout 'wide').
    - Khởi tạo và lưu trữ phiên làm việc (st.session_state).
    - Điều hướng giữa các phân hệ:
        + Trò chơi 15-Puzzle.
        + Tab 1: Quản lý dữ liệu vector (tab_management).
        + Tab 2: Tìm kiếm tương đồng và Benchmark 5 thuật toán (tab_benchmark).
"""
import streamlit as st
from src.ui.tab_puzzle import render_tab_puzzle
from src.ui.tab_management import render_tab1_management
from src.ui.tab_benchmark import render_tab2_benchmark

def main():
    # 1. Cấu hình trang Streamlit
    st.set_page_config(
        page_title="15-Puzzle & Vector Search Engine",
        page_icon="🧩",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # 2. Tiêu đề chính ứng dụng
    st.title("🧩 :rainbow[15-Puzzle] & ⚡ :blue[Vector Search Engine]")
    st.caption("Ứng dụng tích hợp: Trò chơi trượt số 15-Puzzle & Hệ thống tìm kiếm vector tương đồng 5 thuật toán ANN.")

    # 3. Phân chia các Tab: Giữ trọn vẹn 15-Puzzle và bổ sung 2 Tab Vector Search Engine
    tab_puzzle, tab_manage, tab_bench = st.tabs([
        "🧩 Trò chơi 15-Puzzle",
        "📁 Quản lý Dữ liệu Vector (Milvus Core)",
        "⚡ Tìm kiếm & Benchmark 5 Thuật toán (FAISS Core)",
    ])

    with tab_puzzle:
        render_tab_puzzle()

    with tab_manage:
        render_tab1_management()

    with tab_bench:
        render_tab2_benchmark()

if __name__ == "__main__":
    main()
