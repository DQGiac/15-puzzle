"""
Package src.ui: Chứa toàn bộ giao diện Streamlit của dự án.

Các module:
    - tab_puzzle: Giao diện trò chơi 15-Puzzle.
    - tab_management: Tab 1 - Quản lý CSDL vector & Undo (Milvus).
    - tab_benchmark: Tab 2 - Tìm kiếm tương đồng & Benchmark 5 thuật toán (FAISS).
    - app: Bộ điều phối giao diện chính.
"""
from src.ui.tab_puzzle import render_tab_puzzle
from src.ui.tab_management import render_tab1_management
from src.ui.tab_benchmark import render_tab2_benchmark

__all__ = ["render_tab_puzzle", "render_tab1_management", "render_tab2_benchmark"]
