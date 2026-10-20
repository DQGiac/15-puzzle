"""
Module quản lý hệ thống Theme, Styling và Màu sắc cho 15-Puzzle.
Mô phỏng chính xác giao diện C++ Raylib (Catppuccin Mocha / Dark Navy #1E1E2E)
với công thức gradient màu ô số:
    r = 30 + (val * 14)
    g = 60 + (val * 8)
    b = 180 - (val * 6)
Được tối ưu ô vuông hoàn hảo (aspect-ratio 1:1) và khoảng cách xích sát nhau (gap 5px).
"""

import streamlit as st


def generate_tile_css():
    css_rules = []
    for val in range(1, 16):
        r = 30 + val * 14
        g = 60 + val * 8
        b = 180 - val * 6
        css_rules.append(f"""
        .tile-{val} {{
            background: rgb({r}, {g}, {b}) !important;
            color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.25) !important;
        }}
        """)
    return "\n".join(css_rules)


THEME_CSS = f"""
<style>
/* ==========================================================================
   1. C++ RAYLIB COLOR PALETTE (#181825 & #1E1E2E)
   ========================================================================== */
.stApp {{
    background-color: #181825 !important;
    color: #CDD6F4 !important;
}}

/* ==========================================================================
   2. KHUNG TIÊU ĐỀ BÀN CỜ VÀ FOOTER
   ========================================================================== */
.raylib-header-box {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 2px solid #313244;
}}

.raylib-title {{
    color: #FFFFFF;
    font-size: 1.65rem;
    font-weight: 900;
    letter-spacing: 0.06em;
}}

.raylib-timer {{
    color: #C8C8DC;
    font-size: 1.4rem;
    font-weight: 800;
    font-family: 'Courier New', monospace;
}}

.raylib-footer-box {{
    margin-top: 10px;
    padding-top: 8px;
    border-top: 2px solid #313244;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #BAC2DE;
    font-size: 1rem;
    font-weight: 700;
}}

.raylib-solving-status {{
    color: #F9E2AF;
    font-weight: 800;
    margin-top: 6px;
    font-size: 0.95rem;
}}

/* ==========================================================================
   3. NÚT Ô CỜ VUÔNG HOÀN HẢO 1:1 (.c-square-tile)
   ========================================================================== */
.c-square-tile {{
    aspect-ratio: 1 / 1 !important;
    width: 100% !important;
    padding: 0px !important;
    margin: 0px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 12px !important;
    border: none !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    transition: transform 0.08s ease, filter 0.08s ease !important;
}}

.c-square-tile p {{
    font-size: 1.95rem !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    margin: 0px !important;
    padding: 0px !important;
    white-space: nowrap !important;
}}

.c-square-tile:hover:not(:disabled) {{
    transform: translateY(-2px) scale(1.02) !important;
    filter: brightness(1.15) !important;
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
    cursor: pointer !important;
}}

.c-square-tile:disabled {{
    background: #181825 !important;
    background-color: #181825 !important;
    border: 2px dashed #313244 !important;
    box-shadow: inset 0 3px 8px rgba(0, 0, 0, 0.6) !important;
    opacity: 0.35 !important;
    cursor: default !important;
}}

/* ==========================================================================
   4. TIÊU ĐỀ CHÍNH, METRICS, TABS & BẢNG XẾP HẠNG
   ========================================================================== */
.app-title-gradient {{
    background: linear-gradient(135deg, #89B4FA 0%, #CBA6F7 50%, #F38BA8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900;
    font-size: 2.2rem;
    letter-spacing: -0.02em;
}}

[data-testid="stMetric"] {{
    background-color: #1E1E2E !important;
    border: 1.5px solid #313244 !important;
    border-radius: 14px !important;
    padding: 12px !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    border-bottom: 2px solid #313244;
}}

.stTabs [data-baseweb="tab"] {{
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 10px 18px !important;
    border-radius: 10px 10px 0 0 !important;
}}

.leaderboard-card {{
    background: #1E1E2E;
    border: 1.5px solid #313244;
    border-radius: 14px;
    overflow: hidden;
    margin-top: 10px;
}}

.leaderboard-table {{
    width: 100%;
    border-collapse: collapse;
    color: #CDD6F4;
}}

.leaderboard-table th {{
    background: #181825;
    padding: 12px 16px;
    text-align: left;
    color: #A6ADC8;
    text-transform: uppercase;
    font-size: 0.82rem;
    letter-spacing: 0.05em;
    border-bottom: 2px solid #313244;
}}

.leaderboard-table td {{
    padding: 12px 16px;
    border-bottom: 1px solid #313244;
    font-weight: 600;
}}

.badge-steps {{
    background: #313244;
    color: #89B4FA;
    padding: 3px 10px;
    border-radius: 14px;
    font-weight: 800;
}}

{generate_tile_css()}
</style>
"""


def inject_theme_system():
    """Nhúng CSS C++ Raylib chuẩn vào ứng dụng."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)
