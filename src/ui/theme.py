"""
Module quản lý hệ thống Theme (Light/Dark) với hiệu ứng Circular Reveal Animation.
Tích hợp giao diện C++ Raylib Catppuccin Mocha (#1E1E2E) và Crisp Modern Light Theme.
Được tối ưu hóa ô vuông hoàn hảo (aspect-ratio 1:1), khoảng cách 5px và gradient C++ chuẩn:
    r = 30 + val * 14
    g = 60 + val * 8
    b = 180 - val * 6
"""

import streamlit as st
import streamlit.components.v1 as components


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
        html[data-theme="light"] .tile-{val} {{
            background: rgb({r}, {g}, {b}) !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.35) !important;
        }}
        """)
    return "\n".join(css_rules)


THEME_CSS_BASE = """
/* ==========================================================================
   1. RESET & BASE THEME VARIABLES
   ========================================================================== */
:root {
    --bg-main: #0B0F19;
    --bg-card: #1E293B;
    --text-primary: #CDD6F4;
    --text-secondary: #94A3B8;
    --border-color: #313244;
    --border-strong: #475569;
}

/* ==========================================================================
   2. VIEW TRANSITIONS API: CIRCULAR REVEAL ANIMATION
   ========================================================================== */
::view-transition-old(root),
::view-transition-new(root) {
    animation: none;
    mix-blend-mode: normal;
}
::view-transition-old(root) {
    z-index: 1;
}
::view-transition-new(root) {
    z-index: 9999999;
}

.theme-circular-reveal-overlay {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    z-index: 99999999;
    pointer-events: none;
    transition: clip-path 650ms cubic-bezier(0.22, 1, 0.36, 1);
}

/* ==========================================================================
   3. GENERAL STYLING & FONTS (APP-WIDE)
   ========================================================================== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap');

html, body {
    transition: background-color 0.25s ease, color 0.25s ease;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* Custom scrollbars */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #11111B;
}
::-webkit-scrollbar-thumb {
    background: #313244;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #45475A;
}

html[data-theme="light"] ::-webkit-scrollbar-track {
    background: #F1F5F9;
}
html[data-theme="light"] ::-webkit-scrollbar-thumb {
    background: #CBD5E1;
}
html[data-theme="light"] ::-webkit-scrollbar-thumb:hover {
    background: #94A3B8;
}

/* ==========================================================================
   4. THEME TOGGLE BUTTON UI (Top-Right Floating Header)
   ========================================================================== */
#theme-toggle-root {
    position: fixed;
    top: 12px;
    right: 175px;
    z-index: 999999;
    display: flex;
    align-items: center;
    justify-content: center;
}

@media (max-width: 768px) {
    #theme-toggle-root {
        top: 12px;
        right: 56px;
    }
}

.theme-toggle-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 42px;
    height: 42px;
    border-radius: 50%;
    cursor: pointer;
    outline: none;
    padding: 0;
    transition: transform 0.25s cubic-bezier(0.22, 1, 0.36, 1),
                border-color 0.25s ease,
                background-color 0.25s ease,
                box-shadow 0.25s ease;
}

html[data-theme="light"] .theme-toggle-btn {
    background: #FFFFFF;
    border: 2px solid #CBD5E1;
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.12);
    color: #0F172A;
}

html[data-theme="dark"] .theme-toggle-btn,
:root:not([data-theme="light"]) .theme-toggle-btn {
    background: #1E293B;
    border: 2px solid #475569;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.45);
    color: #F8FAFC;
}

.theme-toggle-btn:hover {
    transform: scale(1.12);
    border-color: #0284C7 !important;
    box-shadow: 0 0 16px rgba(2, 132, 199, 0.5) !important;
}

.theme-toggle-btn:active {
    transform: scale(0.95);
}

.theme-toggle-icon {
    width: 22px;
    height: 22px;
    transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.2s ease;
}

.theme-toggle-btn:hover .theme-toggle-icon {
    transform: rotate(25deg);
}

/* ==========================================================================
   5. DARK THEME (CATPPUCCIN MOCHA / RAYLIB C++ PALETTE)
   ========================================================================== */
.stApp {
    background: radial-gradient(ellipse at 50% 0%, #1e1e38 0%, #181825 60%, #11111b 100%) !important;
    background-attachment: fixed !important;
    color: #CDD6F4 !important;
}

/* Khung tiêu đề bàn cờ và footer */
.raylib-header-box {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 2px solid #313244;
}

.raylib-title {
    color: #FFFFFF;
    font-size: 1.65rem;
    font-weight: 900;
    letter-spacing: 0.06em;
}

.raylib-timer {
    color: #C8C8DC;
    font-size: 1.4rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
}

.raylib-footer-box {
    margin-top: 10px;
    padding-top: 8px;
    border-top: 2px solid #313244;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #BAC2DE;
    font-size: 1rem;
    font-weight: 700;
}

.raylib-solving-status {
    color: #F9E2AF;
    font-weight: 800;
    margin-top: 6px;
    font-size: 0.95rem;
}

/* Khung container bàn cờ Catppuccin */
.c-raylib-board-container {
    background: #1E1E2E !important;
    border: 2px solid #313244 !important;
    border-radius: 18px !important;
    padding: 14px !important;
    max-width: 420px !important;
    margin: 0 auto 12px auto !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.55) !important;
    box-sizing: border-box !important;
}

/* Nút ô cờ vuông hoàn hảo 1:1 (.c-square-tile) */
.c-square-tile {
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
}

.c-square-tile p {
    font-size: 1.95rem !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    margin: 0px !important;
    padding: 0px !important;
    white-space: nowrap !important;
}

.c-square-tile:hover:not(:disabled) {
    transform: translateY(-2px) scale(1.02) !important;
    filter: brightness(1.15) !important;
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
    cursor: pointer !important;
}

.c-square-tile:disabled {
    background: #181825 !important;
    background-color: #181825 !important;
    border: 2px dashed #313244 !important;
    box-shadow: inset 0 3px 8px rgba(0, 0, 0, 0.6) !important;
    opacity: 0.35 !important;
    cursor: default !important;
}

/* Hero Header Banner Hiện Đại */
.hero-header-card {
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
}

.hero-title-area {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.app-title-gradient {
    background: linear-gradient(135deg, #89B4FA 0%, #CBA6F7 45%, #F5C2E7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900;
    font-size: 2.25rem;
    letter-spacing: -0.02em;
    line-height: 1.2;
    margin: 0;
}

.hero-subtitle {
    color: #A6ADC8;
    font-size: 0.98rem;
    font-weight: 500;
    margin: 0;
}

.hero-badges-group {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    align-items: center;
}

.tech-pill {
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
}

.tech-pill.accent-blue {
    border-color: rgba(137, 180, 250, 0.5);
    color: #89B4FA;
    background: rgba(137, 180, 250, 0.12);
}

.tech-pill.accent-purple {
    border-color: rgba(203, 166, 247, 0.5);
    color: #CBA6F7;
    background: rgba(203, 166, 247, 0.12);
}

.tech-pill.accent-gold {
    border-color: rgba(249, 226, 175, 0.5);
    color: #F9E2AF;
    background: rgba(249, 226, 175, 0.12);
}

/* Hệ thống Tabs Floating */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(24, 24, 37, 0.85) !important;
    backdrop-filter: blur(12px) !important;
    padding: 6px !important;
    border-radius: 16px !important;
    border: 1.5px solid #313244 !important;
    gap: 8px !important;
    margin-bottom: 24px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px !important;
    color: #A6ADC8 !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 12px 24px !important;
    border: 1px solid transparent !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    background: transparent !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #FFFFFF !important;
    background: rgba(49, 50, 68, 0.45) !important;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(137, 180, 250, 0.2) 0%, rgba(203, 166, 247, 0.2) 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(137, 180, 250, 0.45) !important;
    box-shadow: 0 4px 16px rgba(137, 180, 250, 0.25) !important;
}

.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* Nút Bấm (Buttons) - Loại trừ 16 ô cờ */
button[kind="secondary"]:not(.c-square-tile) {
    background: linear-gradient(180deg, #252639 0%, #1c1d2e 100%) !important;
    border: 1.5px solid #363852 !important;
    border-radius: 12px !important;
    color: #CDD6F4 !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 9px 18px !important;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.16s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

button[kind="secondary"]:not(.c-square-tile):hover:not(:disabled) {
    transform: translateY(-2px) !important;
    border-color: #89B4FA !important;
    color: #89B4FA !important;
    background: #2b2c44 !important;
    box-shadow: 0 6px 18px rgba(137, 180, 250, 0.25) !important;
}

button[kind="secondary"]:not(.c-square-tile):active:not(:disabled) {
    transform: translateY(0px) !important;
}

button[kind="primary"]:not(.c-square-tile) {
    background: linear-gradient(135deg, #89B4FA 0%, #74C7EC 50%, #B4BEFE 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #11111B !important;
    font-weight: 800 !important;
    font-size: 0.96rem !important;
    padding: 10px 22px !important;
    box-shadow: 0 4px 16px rgba(137, 180, 250, 0.4) !important;
    transition: all 0.16s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

button[kind="primary"]:not(.c-square-tile):hover:not(:disabled) {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 26px rgba(137, 180, 250, 0.6) !important;
    filter: brightness(1.08) !important;
}

button[kind="primary"]:not(.c-square-tile):active:not(:disabled) {
    transform: translateY(0px) !important;
}

/* Khung chứa (Containers & Cards Glassmorphism) */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, rgba(30, 30, 46, 0.65) 0%, rgba(24, 24, 37, 0.75) 100%) !important;
    backdrop-filter: blur(12px) !important;
    border: 1.5px solid rgba(137, 180, 250, 0.16) !important;
    border-radius: 18px !important;
    padding: 8px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.38) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(137, 180, 250, 0.3) !important;
    box-shadow: 0 10px 36px rgba(0, 0, 0, 0.45) !important;
}

/* Thẻ Thống Kê (Metrics Cyberpunk) */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1e1e34 0%, #161626 100%) !important;
    border: 1.5px solid #313244 !important;
    border-radius: 16px !important;
    padding: 14px 18px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35) !important;
    transition: transform 0.15s ease, border-color 0.15s ease !important;
}

[data-testid="stMetric"]:hover {
    border-color: #89B4FA !important;
    transform: translateY(-2px) !important;
}

[data-testid="stMetricLabel"] {
    color: #A6ADC8 !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

[data-testid="stMetricValue"] {
    color: #89B4FA !important;
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
    font-weight: 900 !important;
    font-size: 1.65rem !important;
    text-shadow: 0 0 12px rgba(137, 180, 250, 0.25) !important;
}

/* Bảng Xếp Hạng & Podium Ranks */
.leaderboard-card {
    background: #1E1E2E;
    border: 1.5px solid #313244;
    border-radius: 18px;
    overflow: hidden;
    margin-top: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
}

.leaderboard-table {
    width: 100%;
    border-collapse: collapse;
    color: #CDD6F4;
}

.leaderboard-table th {
    background: #181825;
    padding: 14px 18px;
    text-align: left;
    color: #A6ADC8;
    text-transform: uppercase;
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    border-bottom: 2px solid #313244;
    font-weight: 800;
}

.leaderboard-table td {
    padding: 14px 18px;
    border-bottom: 1px solid rgba(49, 50, 68, 0.7);
    font-weight: 600;
    font-size: 0.95rem;
}

.leaderboard-table tr.rank-1 {
    background: linear-gradient(90deg, rgba(249, 226, 175, 0.18) 0%, rgba(249, 226, 175, 0.03) 100%) !important;
}
.leaderboard-table tr.rank-1 td:first-child {
    color: #F9E2AF !important;
    font-weight: 900 !important;
    text-shadow: 0 0 12px rgba(249, 226, 175, 0.5) !important;
}

.leaderboard-table tr.rank-2 {
    background: linear-gradient(90deg, rgba(205, 214, 244, 0.12) 0%, rgba(205, 214, 244, 0.02) 100%) !important;
}
.leaderboard-table tr.rank-2 td:first-child {
    color: #BAC2DE !important;
    font-weight: 900 !important;
    text-shadow: 0 0 10px rgba(186, 194, 222, 0.4) !important;
}

.leaderboard-table tr.rank-3 {
    background: linear-gradient(90deg, rgba(250, 179, 135, 0.14) 0%, rgba(250, 179, 135, 0.02) 100%) !important;
}
.leaderboard-table tr.rank-3 td:first-child {
    color: #FAB387 !important;
    font-weight: 900 !important;
    text-shadow: 0 0 10px rgba(250, 179, 135, 0.4) !important;
}

.badge-steps {
    background: rgba(137, 180, 250, 0.15);
    border: 1px solid rgba(137, 180, 250, 0.35);
    color: #89B4FA;
    padding: 4px 12px;
    border-radius: 16px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
}

/* Benchmark Cards & Chips */
.bench-stats-grid {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 12px 0;
}

.bench-stat-chip {
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
}

.chip-label {
    font-size: 0.78rem;
    color: #A6ADC8;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.04em;
}

.chip-val {
    font-size: 1.2rem;
    color: #89B4FA;
    font-weight: 900;
    font-family: 'JetBrains Mono', monospace;
}

.bench-card-ida {
    background: linear-gradient(145deg, rgba(24, 24, 37, 0.95) 0%, rgba(20, 20, 32, 0.95) 100%);
    border: 1.5px solid rgba(137, 180, 250, 0.35);
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.bench-card-astar {
    background: linear-gradient(145deg, rgba(24, 24, 37, 0.95) 0%, rgba(20, 20, 32, 0.95) 100%);
    border: 1.5px solid rgba(243, 139, 168, 0.35);
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

/* Alerts, Progress, Inputs, Expander */
[data-testid="stAlert"] {
    border-radius: 14px !important;
    font-weight: 600 !important;
    backdrop-filter: blur(10px) !important;
    border-width: 1.5px !important;
}

[data-testid="stProgress"] > div > div > div {
    background: linear-gradient(90deg, #89B4FA 0%, #CBA6F7 50%, #F5C2E7 100%) !important;
    border-radius: 10px !important;
    box-shadow: 0 0 12px rgba(137, 180, 250, 0.5) !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background-color: #181825 !important;
    border: 1.5px solid #313244 !important;
    border-radius: 12px !important;
    color: #CDD6F4 !important;
    font-weight: 600 !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #89B4FA !important;
    box-shadow: 0 0 10px rgba(137, 180, 250, 0.35) !important;
}

[data-testid="stExpander"] {
    background-color: rgba(24, 24, 37, 0.8) !important;
    border: 1.5px solid #313244 !important;
    border-radius: 14px !important;
}

/* ==========================================================================
   6. LIGHT THEME STYLES (html[data-theme="light"])
   ========================================================================== */
html[data-theme="light"],
html[data-theme="light"] body,
html[data-theme="light"] .stApp {
    background: #F8FAFC !important;
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}

html[data-theme="light"] h1,
html[data-theme="light"] h2,
html[data-theme="light"] h3,
html[data-theme="light"] h4,
html[data-theme="light"] h5,
html[data-theme="light"] h6 {
    color: #0F172A !important;
    font-weight: 800 !important;
}

html[data-theme="light"] p,
html[data-theme="light"] span,
html[data-theme="light"] label,
html[data-theme="light"] div {
    color: inherit;
}

html[data-theme="light"] .stCaption,
html[data-theme="light"] [data-testid="stCaptionContainer"] p,
html[data-theme="light"] small {
    color: #475569 !important;
    font-weight: 600 !important;
}

/* Light Mode: Hero Header */
html[data-theme="light"] .hero-header-card {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.08) !important;
}

html[data-theme="light"] .app-title-gradient {
    background: linear-gradient(135deg, #2563EB 0%, #7C3AED 50%, #DB2777 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

html[data-theme="light"] .hero-subtitle {
    color: #475569 !important;
}

html[data-theme="light"] .tech-pill {
    background: #F1F5F9 !important;
    border: 1px solid #CBD5E1 !important;
    color: #334155 !important;
    box-shadow: 0 2px 4px rgba(15, 23, 42, 0.05) !important;
}

html[data-theme="light"] .tech-pill.accent-blue {
    background: #E0F2FE !important;
    border-color: #BAE6FD !important;
    color: #0284C7 !important;
}

html[data-theme="light"] .tech-pill.accent-purple {
    background: #F3E8FF !important;
    border-color: #E9D5FF !important;
    color: #7C3AED !important;
}

html[data-theme="light"] .tech-pill.accent-gold {
    background: #FEF3C7 !important;
    border-color: #FDE68A !important;
    color: #D97706 !important;
}

/* Light Mode: Tabs */
html[data-theme="light"] .stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06) !important;
}

html[data-theme="light"] .stTabs [data-baseweb="tab"] {
    color: #475569 !important;
}

html[data-theme="light"] .stTabs [data-baseweb="tab"]:hover {
    color: #0F172A !important;
    background: #F1F5F9 !important;
}

html[data-theme="light"] .stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.12) 0%, rgba(124, 58, 237, 0.12) 100%) !important;
    color: #1D4ED8 !important;
    border: 1px solid rgba(37, 99, 235, 0.35) !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15) !important;
}

/* Light Mode: Buttons (Loại trừ 16 ô cờ vuông .c-square-tile) */
html[data-theme="light"] button[kind="secondary"]:not(.c-square-tile),
html[data-theme="light"] .stButton > button:not(.c-square-tile) {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 5px rgba(15, 23, 42, 0.08) !important;
    transition: all 0.12s ease !important;
}

html[data-theme="light"] button[kind="secondary"]:not(.c-square-tile):hover:not(:disabled),
html[data-theme="light"] .stButton > button:not(.c-square-tile):hover:not(:disabled) {
    border-color: #0284C7 !important;
    color: #0284C7 !important;
    background: #F8FAFC !important;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.2) !important;
    transform: translateY(-2px) !important;
}

html[data-theme="light"] button[kind="primary"]:not(.c-square-tile) {
    background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35) !important;
}

html[data-theme="light"] button[kind="primary"]:not(.c-square-tile):hover:not(:disabled) {
    filter: brightness(1.1) !important;
    box-shadow: 0 6px 20px rgba(2, 132, 199, 0.5) !important;
    transform: translateY(-2px) !important;
}

/* Light Mode: Bàn cờ C++ Frame & Square Tiles */
html[data-theme="light"] .c-raylib-board-container {
    background: #FFFFFF !important;
    border: 2px solid #CBD5E1 !important;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08) !important;
}

html[data-theme="light"] .raylib-header-box {
    border-bottom: 2px solid #CBD5E1 !important;
}

html[data-theme="light"] .raylib-title {
    color: #0F172A !important;
}

html[data-theme="light"] .raylib-timer {
    color: #334155 !important;
}

html[data-theme="light"] .raylib-footer-box {
    border-top: 2px solid #CBD5E1 !important;
    color: #475569 !important;
}

html[data-theme="light"] .raylib-solving-status {
    color: #D97706 !important;
}

html[data-theme="light"] .c-square-tile:disabled {
    background: #E2E8F0 !important;
    background-color: #E2E8F0 !important;
    border: 2.5px dashed #94A3B8 !important;
    box-shadow: inset 0 3px 8px rgba(0, 0, 0, 0.08) !important;
    opacity: 0.65 !important;
}

/* Light Mode: Containers Glassmorphism */
html[data-theme="light"] [data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.06) !important;
}

html[data-theme="light"] [data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #94A3B8 !important;
}

/* Light Mode: Metrics */
html[data-theme="light"] [data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06) !important;
}

html[data-theme="light"] [data-testid="stMetric"]:hover {
    border-color: #0284C7 !important;
}

html[data-theme="light"] [data-testid="stMetricLabel"] {
    color: #475569 !important;
}

html[data-theme="light"] [data-testid="stMetricValue"] {
    color: #0284C7 !important;
    text-shadow: none !important;
}

/* Light Mode: Leaderboard */
html[data-theme="light"] .leaderboard-card {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06) !important;
}

html[data-theme="light"] .leaderboard-table {
    color: #0F172A !important;
}

html[data-theme="light"] .leaderboard-table th {
    background: #F8FAFC !important;
    color: #475569 !important;
    border-bottom: 2px solid #CBD5E1 !important;
}

html[data-theme="light"] .leaderboard-table td {
    border-bottom: 1px solid #F1F5F9 !important;
    color: #0F172A !important;
}

html[data-theme="light"] .leaderboard-table strong {
    color: #0F172A !important;
}

html[data-theme="light"] .leaderboard-table tr:hover td {
    background: #F8FAFC !important;
}

html[data-theme="light"] .badge-steps {
    background: #E0F2FE !important;
    border: 1px solid #BAE6FD !important;
    color: #0369A1 !important;
}

html[data-theme="light"] .leaderboard-table tr.rank-1 {
    background: linear-gradient(90deg, rgba(254, 243, 199, 0.45) 0%, rgba(254, 243, 199, 0.08) 100%) !important;
}
html[data-theme="light"] .leaderboard-table tr.rank-1 td:first-child {
    color: #B45309 !important;
    text-shadow: none !important;
}

html[data-theme="light"] .leaderboard-table tr.rank-2 {
    background: linear-gradient(90deg, rgba(241, 245, 249, 0.8) 0%, rgba(241, 245, 249, 0.15) 100%) !important;
}
html[data-theme="light"] .leaderboard-table tr.rank-2 td:first-child {
    color: #475569 !important;
    text-shadow: none !important;
}

html[data-theme="light"] .leaderboard-table tr.rank-3 {
    background: linear-gradient(90deg, rgba(254, 215, 170, 0.35) 0%, rgba(254, 215, 170, 0.08) 100%) !important;
}
html[data-theme="light"] .leaderboard-table tr.rank-3 td:first-child {
    color: #C2410C !important;
    text-shadow: none !important;
}

/* Light Mode: Benchmark Cards & Chips */
html[data-theme="light"] .bench-stat-chip {
    background: #F8FAFC !important;
    border: 1.5px solid #CBD5E1 !important;
    box-shadow: inset 0 1px 3px rgba(15, 23, 42, 0.05) !important;
}

html[data-theme="light"] .chip-label {
    color: #475569 !important;
}

html[data-theme="light"] .chip-val {
    color: #0284C7 !important;
}

html[data-theme="light"] .bench-card-ida {
    background: #FFFFFF !important;
    border: 1.5px solid #BAE6FD !important;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.08) !important;
}

html[data-theme="light"] .bench-card-astar {
    background: #FFFFFF !important;
    border: 1.5px solid #FBCFE8 !important;
    box-shadow: 0 4px 14px rgba(219, 39, 119, 0.08) !important;
}

html[data-theme="light"] .mini-board-wrapper {
    background: #FFFFFF !important;
    border: 2px solid #CBD5E1 !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08) !important;
}

html[data-theme="light"] .mini-empty {
    background: #E2E8F0 !important;
    border: 1.5px dashed #94A3B8 !important;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.08) !important;
}

/* Light Mode: Expander, Inputs & Alerts */
html[data-theme="light"] [data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
}

html[data-theme="light"] [data-testid="stTextInput"] input,
html[data-theme="light"] [data-testid="stTextArea"] textarea {
    background-color: #F8FAFC !important;
    border: 1.5px solid #CBD5E1 !important;
    color: #0F172A !important;
}

html[data-theme="light"] [data-testid="stTextInput"] input:focus,
html[data-theme="light"] [data-testid="stTextArea"] textarea:focus {
    border-color: #0284C7 !important;
    box-shadow: 0 0 8px rgba(2, 132, 199, 0.25) !important;
}

html[data-theme="light"] [data-testid="stAlert"] {
    background-color: #EFF6FF !important;
    border: 1.5px solid #93C5FD !important;
    color: #1E3A8A !important;
}
"""

THEME_CSS = THEME_CSS_BASE + "\n" + generate_tile_css()


THEME_JS = """
<script>
(function() {
    const doc = window.parent.document;
    const win = window.parent;

    if (!doc || !win) return;

    // 1. Cập nhật Icon nút Toggle (Sun / Moon)
    win.__stUpdateButtonUI = function(theme) {
        const btn = doc.getElementById('theme-toggle-btn');
        if (!btn) return;

        if (theme === 'dark') {
            btn.innerHTML = `
                <svg class="theme-toggle-icon" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="5"></circle>
                    <line x1="12" y1="1" x2="12" y2="3"></line>
                    <line x1="12" y1="21" x2="12" y2="23"></line>
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                    <line x1="1" y1="12" x2="3" y2="12"></line>
                    <line x1="21" y1="12" x2="23" y2="12"></line>
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
                </svg>
            `;
            btn.setAttribute('title', 'Chuyển sang Chế độ Sáng (Light Mode)');
        } else {
            btn.innerHTML = `
                <svg class="theme-toggle-icon" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
            `;
            btn.setAttribute('title', 'Chuyển sang Chế độ Tối (Dark Mode)');
        }
    };

    // 2. Áp dụng theme vào toàn bộ DOM
    win.__stApplyThemeToDOM = function(theme) {
        doc.documentElement.setAttribute('data-theme', theme);
        if (doc.body) {
            doc.body.setAttribute('data-theme', theme);
        }
        const appContainer = doc.querySelector('.stApp');
        if (appContainer) {
            appContainer.setAttribute('data-theme', theme);
        }

        // Cập nhật khung bàn cờ C++ nếu đã render
        const boardCont = doc.querySelector('.c-raylib-board-container');
        if (boardCont) {
            if (theme === 'light') {
                boardCont.style.setProperty('background', '#FFFFFF', 'important');
                boardCont.style.setProperty('border', '2px solid #CBD5E1', 'important');
                boardCont.style.setProperty('box-shadow', '0 8px 24px rgba(15, 23, 42, 0.08)', 'important');
            } else {
                boardCont.style.setProperty('background', '#1E1E2E', 'important');
                boardCont.style.setProperty('border', '2px solid #313244', 'important');
                boardCont.style.setProperty('box-shadow', '0 12px 30px rgba(0,0,0,0.55)', 'important');
            }
        }

        try {
            win.localStorage.setItem('st_theme_mode', theme);
        } catch (e) {}
        win.__stUpdateButtonUI(theme);
    };

    // 3. Hiệu ứng Circular Reveal Animation cốt lõi
    win.__stTriggerCircularReveal = function(event) {
        try {
            let currentTheme = 'dark';
            try {
                currentTheme = win.localStorage.getItem('st_theme_mode') || 'dark';
            } catch (e) {}

            const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
            const btn = doc.getElementById('theme-toggle-btn');

            let x = win.innerWidth - 195;
            let y = 30;
            if (btn) {
                const rect = btn.getBoundingClientRect();
                x = rect.left + rect.width / 2;
                y = rect.top + rect.height / 2;
            } else if (event && event.clientX) {
                x = event.clientX;
                y = event.clientY;
            }

            const endRadius = Math.hypot(
                Math.max(x, win.innerWidth - x),
                Math.max(y, win.innerHeight - y)
            );

            const prefersReducedMotion = win.matchMedia && win.matchMedia('(prefers-reduced-motion: reduce)').matches;
            if (prefersReducedMotion) {
                win.__stApplyThemeToDOM(nextTheme);
                return;
            }

            if (typeof doc.startViewTransition === 'function') {
                const transition = doc.startViewTransition(() => {
                    win.__stApplyThemeToDOM(nextTheme);
                });

                transition.ready.then(() => {
                    const clipAnimation = [
                        `circle(0px at ${x}px ${y}px)`,
                        `circle(${endRadius}px at ${x}px ${y}px)`
                    ];

                    doc.documentElement.animate(
                        { clipPath: clipAnimation },
                        {
                            duration: 650,
                            easing: 'cubic-bezier(0.22, 1, 0.36, 1)',
                            pseudoElement: '::view-transition-new(root)'
                        }
                    );
                }).catch(() => {});
            } else {
                const overlay = doc.createElement('div');
                overlay.className = 'theme-circular-reveal-overlay';
                overlay.style.backgroundColor = nextTheme === 'dark' ? '#181825' : '#F8FAFC';
                overlay.style.clipPath = `circle(0px at ${x}px ${y}px)`;
                doc.body.appendChild(overlay);

                void overlay.offsetWidth;
                overlay.style.clipPath = `circle(${endRadius}px at ${x}px ${y}px)`;

                setTimeout(() => {
                    win.__stApplyThemeToDOM(nextTheme);
                }, 320);

                setTimeout(() => {
                    if (overlay.parentNode) {
                        overlay.parentNode.removeChild(overlay);
                    }
                }, 700);
            }
        } catch (err) {
            console.error("Theme toggle error:", err);
        }
    };

    // 4. Khởi tạo nút Toggle trên Header
    function setupButton() {
        let toggleContainer = doc.getElementById('theme-toggle-root');
        let button = doc.getElementById('theme-toggle-btn');

        if (!toggleContainer) {
            toggleContainer = doc.createElement('div');
            toggleContainer.id = 'theme-toggle-root';
            button = doc.createElement('button');
            button.id = 'theme-toggle-btn';
            button.className = 'theme-toggle-btn';
            toggleContainer.appendChild(button);
            doc.body.appendChild(toggleContainer);
        }

        if (button) {
            button.onclick = function(e) {
                if (e) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                win.__stTriggerCircularReveal(e);
            };
        }

        let savedTheme = 'dark';
        try {
            const search = win.location.search;
            if (search.includes('theme=dark')) {
                savedTheme = 'dark';
            } else if (search.includes('theme=light')) {
                savedTheme = 'light';
            } else {
                savedTheme = win.localStorage.getItem('st_theme_mode') || 'dark';
            }
        } catch (e) {
            savedTheme = 'dark';
        }

        win.__stApplyThemeToDOM(savedTheme);
    }

    setupButton();
    setTimeout(setupButton, 350);
})();
</script>
"""


def inject_theme_system():
    """
    Tiêm toàn bộ hệ thống CSS Theme (Light/Dark) và Nút Toggle Circular Reveal vào Streamlit.
    """
    st.html(f'<style id="st-theme-system-css">{THEME_CSS}</style>')
    components.html(THEME_JS, height=0, width=0)
