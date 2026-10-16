import sys
from pathlib import Path
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.ui.theme import inject_theme_system
from src.ui.tab_puzzle import render_tab_puzzle

st.set_page_config(
    page_title="15-Puzzle Game",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_theme_system()
st.title("🧩 :rainbow[15-Puzzle Game]")
render_tab_puzzle()
