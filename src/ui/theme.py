"""
Module quản lý hệ thống Theme, Styling và Màu sắc cho 15-Puzzle.
Mô phỏng chính xác giao diện C++ Raylib (Catppuccin Mocha / Dark Navy #1E1E2E)
với công thức gradient màu ô số:
    r = 30 + (val * 14)
    g = 60 + (val * 8)
    b = 180 - (val * 6)
Được tối ưu ô vuông hoàn hảo (aspect-ratio 1:1) và khoảng cách xích sát nhau (gap 5px).
Bổ sung hệ thống UI/UX hiện đại (Cyberpunk/Glassmorphic) cho toàn bộ hệ thống Tabs,
Cards, Buttons, Metrics, và Bảng Xếp Hạng.
"""

import streamlit as st


def generate_tile_css():
    """Tạo CSS gradient cho từng ô số từ 1 đến 15 chuẩn C++ Raylib."""
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
   1. C++ RAYLIB & CATPPUCCIN MOCHA PALETTE - ATMOSPHERIC BACKGROUND
   ========================================================================== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

.stApp {{
    background: radial-gradient(ellipse at 50% 0%, #1e1e38 0%, #181825 60%, #11111b 100%) !important;
    background-attachment: fixed !important;
    color: #CDD6F4 !important;
}}

/* Custom scrollbar */
::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}
::-webkit-scrollbar-track {{
    background: #11111B;
}}
::-webkit-scrollbar-thumb {{
    background: #313244;
    border-radius: 4px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: #45475A;
}}

/* ==========================================================================
   2. KHUNG TIÊU ĐỀ BÀN CỜ VÀ FOOTER (CHUẨN GỐC RAYLIB - KHÔNG THAY ĐỔI)
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
    font-family: 'JetBrains Mono', 'Courier New', monospace;
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
   3. NÚT Ô CỜ VUÔNG HOÀN HẢO 1:1 (.c-square-tile) (KHÔNG THAY ĐỔI)
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
   4. HERO HEADER BANNER HIỆN ĐẠI
   ========================================================================== */
.hero-header-card {{
    background: linear-gradient(135deg, rgba(30, 30, 46, 0.85) 0%, rgba(24, 24, 37, 0.95) 100%);
    border: 1.5px solid rgba(137, 180, 250, 0.2);
    border-radius: 20px;
    padding: 22px 28px;
    margin-bottom: 22px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}}

.hero-title-area {{
    display: flex;
    flex-direction: column;
    gap: 6px;
}}

.app-title-gradient {{
    background: linear-gradient(135deg, #89B4FA 0%, #CBA6F7 45%, #F5C2E7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900;
    font-size: 2.25rem;
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin: 0;
}}

.hero-subtitle {{
    color: #A6ADC8;
    font-size: 0.98rem;
    font-weight: 500;
    margin: 0;
}}

.hero-badges-group {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    align-items: center;
}}

.tech-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 700;
    background: rgba(49, 50, 68, 0.55);
    border: 1px solid rgba(137, 180, 250, 0.25);
    color: #CDD6F4;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}}

.tech-pill.accent-blue {{
    border-color: rgba(137, 180, 250, 0.5);
    color: #89B4FA;
    background: rgba(137, 180, 250, 0.12);
}}

.tech-pill.accent-purple {{
    border-color: rgba(203, 166, 247, 0.5);
    color: #CBA6F7;
    background: rgba(203, 166, 247, 0.12);
}}

.tech-pill.accent-gold {{
    border-color: rgba(249, 226, 175, 0.5);
    color: #F9E2AF;
    background: rgba(249, 226, 175, 0.12);
}}

/* ==========================================================================
   5. HỆ THỐNG TABS FLOATING HIỆN ĐẠI (PILL / SEGMENTED CONTROL)
   ========================================================================== */
.stTabs [data-baseweb="tab-list"] {{
    background: rgba(24, 24, 37, 0.85) !important;
    backdrop-filter: blur(12px) !important;
    padding: 6px !important;
    border-radius: 16px !important;
    border: 1.5px solid #313244 !important;
    gap: 8px !important;
    margin-bottom: 24px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35) !important;
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: 12px !important;
    color: #A6ADC8 !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 12px 24px !important;
    border: 1px solid transparent !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    background: transparent !important;
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: #FFFFFF !important;
    background: rgba(49, 50, 68, 0.45) !important;
}}

.stTabs [data-baseweb="tab"][aria-selected="true"] {{
    background: linear-gradient(135deg, rgba(137, 180, 250, 0.2) 0%, rgba(203, 166, 247, 0.2) 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(137, 180, 250, 0.45) !important;
    box-shadow: 0 4px 16px rgba(137, 180, 250, 0.25) !important;
}}

/* Ẩn thanh gạch chân mặc định của Streamlit tab */
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {{
    display: none !important;
}}

/* ==========================================================================
   6. NÚT BẤM (BUTTONS) - LOẠI TRỪ 16 Ô CỜ BẰNG :not(.c-square-tile)
   ========================================================================== */
/* Nút Secondary chuẩn Streamlit */
button[kind="secondary"]:not(.c-square-tile) {{
    background: linear-gradient(180deg, #252639 0%, #1c1d2e 100%) !important;
    border: 1.5px solid #363852 !important;
    border-radius: 12px !important;
    color: #CDD6F4 !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 9px 18px !important;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.16s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

button[kind="secondary"]:not(.c-square-tile):hover:not(:disabled) {{
    transform: translateY(-2px) !important;
    border-color: #89B4FA !important;
    color: #89B4FA !important;
    background: #2b2c44 !important;
    box-shadow: 0 6px 18px rgba(137, 180, 250, 0.25) !important;
}}

button[kind="secondary"]:not(.c-square-tile):active:not(:disabled) {{
    transform: translateY(0px) !important;
}}

/* Nút Primary (Nổi bật - Xanh Cyan / Gradient) */
button[kind="primary"]:not(.c-square-tile) {{
    background: linear-gradient(135deg, #89B4FA 0%, #74C7EC 50%, #B4BEFE 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #11111B !important;
    font-weight: 800 !important;
    font-size: 0.96rem !important;
    padding: 10px 22px !important;
    box-shadow: 0 4px 16px rgba(137, 180, 250, 0.4) !important;
    transition: all 0.16s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

button[kind="primary"]:not(.c-square-tile):hover:not(:disabled) {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 26px rgba(137, 180, 250, 0.6) !important;
    filter: brightness(1.08) !important;
}}

button[kind="primary"]:not(.c-square-tile):active:not(:disabled) {{
    transform: translateY(0px) !important;
}}

/* ==========================================================================
   7. KHUNG CHỨA (CONTAINERS & CARDS GLASSMORPHISM)
   ========================================================================== */
[data-testid="stVerticalBlockBorderWrapper"] {{
    background: linear-gradient(145deg, rgba(30, 30, 46, 0.65) 0%, rgba(24, 24, 37, 0.75) 100%) !important;
    backdrop-filter: blur(12px) !important;
    border: 1.5px solid rgba(137, 180, 250, 0.16) !important;
    border-radius: 18px !important;
    padding: 8px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.38) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    border-color: rgba(137, 180, 250, 0.3) !important;
    box-shadow: 0 10px 36px rgba(0, 0, 0, 0.45) !important;
}}

/* ==========================================================================
   8. THẺ THỐNG KÊ (METRICS CYBERPUNK)
   ========================================================================== */
[data-testid="stMetric"] {{
    background: linear-gradient(145deg, #1e1e34 0%, #161626 100%) !important;
    border: 1.5px solid #313244 !important;
    border-radius: 16px !important;
    padding: 14px 18px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35) !important;
    transition: transform 0.15s ease, border-color 0.15s ease !important;
}}

[data-testid="stMetric"]:hover {{
    border-color: #89B4FA !important;
    transform: translateY(-2px) !important;
}}

[data-testid="stMetricLabel"] {{
    color: #A6ADC8 !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}}

[data-testid="stMetricValue"] {{
    color: #89B4FA !important;
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    font-weight: 900 !important;
    font-size: 1.65rem !important;
    text-shadow: 0 0 12px rgba(137, 180, 250, 0.25) !important;
}}

/* ==========================================================================
   9. BẢNG XẾP HẠNG & PODIUM RANKS (GOLD, SILVER, BRONZE)
   ========================================================================== */
.leaderboard-card {{
    background: #1E1E2E;
    border: 1.5px solid #313244;
    border-radius: 18px;
    overflow: hidden;
    margin-top: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
}}

.leaderboard-table {{
    width: 100%;
    border-collapse: collapse;
    color: #CDD6F4;
}}

.leaderboard-table th {{
    background: #181825;
    padding: 14px 18px;
    text-align: left;
    color: #A6ADC8;
    text-transform: uppercase;
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    border-bottom: 2px solid #313244;
    font-weight: 800;
}}

.leaderboard-table td {{
    padding: 14px 18px;
    border-bottom: 1px solid rgba(49, 50, 68, 0.7);
    font-weight: 600;
    font-size: 0.95rem;
}}

/* Hạng 1: Vàng Gold */
.leaderboard-table tr.rank-1 {{
    background: linear-gradient(90deg, rgba(249, 226, 175, 0.18) 0%, rgba(249, 226, 175, 0.03) 100%) !important;
}}
.leaderboard-table tr.rank-1 td:first-child {{
    color: #F9E2AF !important;
    font-weight: 900 !important;
    text-shadow: 0 0 12px rgba(249, 226, 175, 0.5) !important;
}}

/* Hạng 2: Bạc Silver */
.leaderboard-table tr.rank-2 {{
    background: linear-gradient(90deg, rgba(205, 214, 244, 0.12) 0%, rgba(205, 214, 244, 0.02) 100%) !important;
}}
.leaderboard-table tr.rank-2 td:first-child {{
    color: #BAC2DE !important;
    font-weight: 900 !important;
    text-shadow: 0 0 10px rgba(186, 194, 222, 0.4) !important;
}}

/* Hạng 3: Đồng Bronze */
.leaderboard-table tr.rank-3 {{
    background: linear-gradient(90deg, rgba(250, 179, 135, 0.14) 0%, rgba(250, 179, 135, 0.02) 100%) !important;
}}
.leaderboard-table tr.rank-3 td:first-child {{
    color: #FAB387 !important;
    font-weight: 900 !important;
    text-shadow: 0 0 10px rgba(250, 179, 135, 0.4) !important;
}}

.badge-steps {{
    background: rgba(137, 180, 250, 0.15);
    border: 1px solid rgba(137, 180, 250, 0.35);
    color: #89B4FA;
    padding: 4px 12px;
    border-radius: 16px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
}}

/* ==========================================================================
   10. CHIPS THÔNG SỐ TOÁN HỌC & BENCHMARK CARDS
   ========================================================================== */
.bench-stats-grid {{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 12px 0;
}}

.bench-stat-chip {{
    background: #181825;
    border: 1.5px solid #313244;
    border-radius: 12px;
    padding: 10px 14px;
    flex: 1;
    min-width: 120px;
    display: flex;
    flex-direction: column;
    gap: 4px;
    box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.4);
}}

.chip-label {{
    font-size: 0.78rem;
    color: #A6ADC8;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.04em;
}}

.chip-val {{
    font-size: 1.2rem;
    color: #89B4FA;
    font-weight: 900;
    font-family: 'JetBrains Mono', monospace;
}}

.bench-card-ida {{
    background: linear-gradient(145deg, rgba(24, 24, 37, 0.95) 0%, rgba(20, 20, 32, 0.95) 100%);
    border: 1.5px solid rgba(137, 180, 250, 0.35);
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}}

.bench-card-astar {{
    background: linear-gradient(145deg, rgba(24, 24, 37, 0.95) 0%, rgba(20, 20, 32, 0.95) 100%);
    border: 1.5px solid rgba(243, 139, 168, 0.35);
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}}

/* ==========================================================================
   11. THÔNG BÁO (ALERTS GLASSMORPHISM)
   ========================================================================== */
[data-testid="stAlert"] {{
    border-radius: 14px !important;
    font-weight: 600 !important;
    backdrop-filter: blur(10px) !important;
    border-width: 1.5px !important;
}}

/* ==========================================================================
   12. THANH TIẾN TRÌNH & ĐIỀU KHIỂN NHẬP LIỆU
   ========================================================================== */
[data-testid="stProgress"] > div > div > div {{
    background: linear-gradient(90deg, #89B4FA 0%, #CBA6F7 50%, #F5C2E7 100%) !important;
    border-radius: 10px !important;
    box-shadow: 0 0 12px rgba(137, 180, 250, 0.5) !important;
}}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {{
    background-color: #181825 !important;
    border: 1.5px solid #313244 !important;
    border-radius: 12px !important;
    color: #CDD6F4 !important;
    font-weight: 600 !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {{
    border-color: #89B4FA !important;
    box-shadow: 0 0 10px rgba(137, 180, 250, 0.35) !important;
}}

/* Expander styling */
[data-testid="stExpander"] {{
    background-color: rgba(24, 24, 37, 0.8) !important;
    border: 1.5px solid #313244 !important;
    border-radius: 14px !important;
}}

{generate_tile_css()}
</style>
"""


def inject_theme_system():
    """Nhúng toàn bộ CSS Dark Catppuccin & Cyberpunk UI vào ứng dụng Streamlit."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)
