"""
Module quản lý hệ thống Theme (Light/Dark) với hiệu ứng Circular Reveal Animation.
Được tối ưu hóa độ tương phản cao, màu sắc sắc nét, chữ to rõ, viền đậm dứt khoát trong cả Light Mode và Dark Mode.
"""
import streamlit as st
import streamlit.components.v1 as components

THEME_CSS = """
/* ==========================================================================
   1. RESET & BASE THEME VARIABLES
   ========================================================================== */
:root {
    --bg-main: #0B0F19;
    --bg-card: #1E293B;
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --border-color: #334155;
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
   3. GENERAL STYLING (APP-WIDE)
   ========================================================================== */
html, body {
    transition: background-color 0.25s ease, color 0.25s ease;
}

[data-testid="stHeader"] {
    background-color: transparent !important;
}

.app-title-gradient {
    background: linear-gradient(135deg, #2563EB 0%, #7C3AED 50%, #DB2777 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900;
    font-size: 2.2rem;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 0.2rem;
    letter-spacing: -0.02em;
}

/* ==========================================================================
   4. LIGHT THEME STYLES (html[data-theme="light"])
   ========================================================================== */
html[data-theme="light"],
html[data-theme="light"] body,
html[data-theme="light"] .stApp {
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

/* TẤT CẢ CÁC NÚT BẤM (BUTTONS) TRONG LIGHT THEME */
html[data-theme="light"] button,
html[data-theme="light"] .stButton > button,
html[data-theme="light"] button[kind="secondary"],
html[data-theme="light"] button[data-testid*="Button"],
html[data-theme="light"] button[data-testid*="baseButton"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 2px solid #94A3B8 !important;
    border-radius: 12px !important;
    font-size: 0.95rem !important;
    font-weight: 800 !important;
    box-shadow: 0 3px 0 #94A3B8, 0 4px 10px rgba(15, 23, 42, 0.1) !important;
    transition: all 0.12s ease !important;
    height: 46px !important;
}

html[data-theme="light"] button p,
html[data-theme="light"] button span,
html[data-theme="light"] button div,
html[data-theme="light"] .stButton > button p,
html[data-theme="light"] .stButton > button span,
html[data-theme="light"] .stButton > button div {
    color: #0F172A !important;
    font-weight: 800 !important;
}

html[data-theme="light"] button:hover,
html[data-theme="light"] .stButton > button:hover {
    border-color: #0284C7 !important;
    color: #0284C7 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 0 #0284C7, 0 6px 14px rgba(2, 132, 199, 0.25) !important;
}

html[data-theme="light"] button:hover p,
html[data-theme="light"] button:hover span,
html[data-theme="light"] .stButton > button:hover p,
html[data-theme="light"] .stButton > button:hover span {
    color: #0284C7 !important;
}

/* Ô CỜ 15-PUZZLE (4x4 GRID) TRONG LIGHT THEME */
/* Ô nằm trong lưới 4x4 (cột con bên trong cột bàn cờ) */
html[data-theme="light"] div[data-testid="stColumn"] div[data-testid="stColumn"] .stButton > button,
html[data-theme="light"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] .stButton > button {
    height: 68px !important;
    font-size: 1.65rem !important;
    font-weight: 900 !important;
    border: 2.5px solid #94A3B8 !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 0 #94A3B8, 0 6px 14px rgba(15, 23, 42, 0.12) !important;
}

html[data-theme="light"] div[data-testid="stColumn"] div[data-testid="stColumn"] .stButton > button p,
html[data-theme="light"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] .stButton > button p {
    font-size: 1.65rem !important;
    font-weight: 900 !important;
    color: #0F172A !important;
}

/* Ô CÓ THỂ DI CHUYỂN (Primary - Sáng rực rỡ nổi bật) */
html[data-theme="light"] button[kind="primary"],
html[data-theme="light"] button[data-testid*="primary"],
html[data-theme="light"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
    background-color: #0284C7 !important;
    color: #FFFFFF !important;
    font-size: 0.95rem !important;
    font-weight: 800 !important;
    border: 2.5px solid #0369A1 !important;
    box-shadow: 0 4px 0 #075985, 0 6px 18px rgba(2, 132, 199, 0.45) !important;
    height: 68px !important;
    cursor: pointer !important;
}

html[data-theme="light"] button[kind="primary"] p,
html[data-theme="light"] button[kind="primary"] span,
html[data-theme="light"] button[kind="primary"] div,
html[data-theme="light"] .stButton > button[kind="primary"] p,
html[data-theme="light"] .stButton > button[kind="primary"] span {
    color: #FFFFFF !important;
    font-weight: 900 !important;
}

html[data-theme="light"] button[kind="primary"]:hover,
html[data-theme="light"] .stButton > button[kind="primary"]:hover {
    filter: brightness(1.12);
    transform: translateY(-2px) !important;
}

/* Ô TRỐNG (Disabled - Hốc 3D) */
html[data-theme="light"] button:disabled,
html[data-theme="light"] .stButton > button:disabled {
    background: #E2E8F0 !important;
    background-color: #E2E8F0 !important;
    border: 2.5px dashed #94A3B8 !important;
    box-shadow: inset 0 3px 8px rgba(0, 0, 0, 0.1) !important;
    opacity: 0.95 !important;
    cursor: default !important;
}

/* THẺ THỐNG SỐ (METRIC) TRONG LIGHT THEME */
html[data-theme="light"] [data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 2px solid #CBD5E1 !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08) !important;
}

html[data-theme="light"] [data-testid="stMetricLabel"] p,
html[data-theme="light"] [data-testid="stMetricLabel"] div {
    color: #475569 !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

html[data-theme="light"] [data-testid="stMetricValue"] div {
    color: #0F172A !important;
    font-size: 2.1rem !important;
    font-weight: 900 !important;
}

/* ALERT & CONTAINERS TRONG LIGHT THEME */
html[data-theme="light"] [data-testid="stAlert"] {
    background-color: #EFF6FF !important;
    border: 2px solid #93C5FD !important;
    color: #1E3A8A !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

html[data-theme="light"] [data-testid="stExpander"],
html[data-theme="light"] div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border: 2px solid #CBD5E1 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06) !important;
}

html[data-theme="light"] [data-testid="stExpander"] summary {
    font-weight: 700 !important;
    color: #0F172A !important;
}

html[data-theme="light"] [data-baseweb="textarea"] {
    background-color: #F8FAFC !important;
    border: 2px solid #CBD5E1 !important;
    border-radius: 10px !important;
    color: #0F172A !important;
}

html[data-theme="light"] [data-baseweb="textarea"] textarea {
    color: #0F172A !important;
    font-weight: 600 !important;
}

/* ==========================================================================
   5. DARK THEME STYLES (html[data-theme="dark"] hoặc mặc định)
   ========================================================================== */
html[data-theme="dark"],
html[data-theme="dark"] body,
html[data-theme="dark"] .stApp,
:root:not([data-theme="light"]) .stApp {
    background-color: #0B0F19 !important;
    color: #F8FAFC !important;
}

html[data-theme="dark"] h1,
html[data-theme="dark"] h2,
html[data-theme="dark"] h3,
html[data-theme="dark"] h4,
html[data-theme="dark"] h5,
html[data-theme="dark"] h6,
:root:not([data-theme="light"]) h1,
:root:not([data-theme="light"]) h2,
:root:not([data-theme="light"]) h3 {
    color: #F8FAFC !important;
    font-weight: 800 !important;
}

html[data-theme="dark"] p,
html[data-theme="dark"] span,
html[data-theme="dark"] label,
html[data-theme="dark"] div,
:root:not([data-theme="light"]) p {
    color: inherit;
}

html[data-theme="dark"] .stCaption,
html[data-theme="dark"] [data-testid="stCaptionContainer"] p,
html[data-theme="dark"] small,
:root:not([data-theme="light"]) .stCaption {
    color: #94A3B8 !important;
    font-weight: 600 !important;
}

/* TẤT CẢ CÁC NÚT BẤM (BUTTONS) TRONG DARK THEME */
html[data-theme="dark"] button,
html[data-theme="dark"] .stButton > button,
html[data-theme="dark"] button[kind="secondary"],
html[data-theme="dark"] button[data-testid*="Button"],
html[data-theme="dark"] button[data-testid*="baseButton"],
:root:not([data-theme="light"]) button,
:root:not([data-theme="light"]) .stButton > button {
    background: #1E293B !important;
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 2px solid #475569 !important;
    border-radius: 12px !important;
    font-size: 0.95rem !important;
    font-weight: 800 !important;
    box-shadow: 0 3px 0 #0F172A, 0 4px 10px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.12s ease !important;
    height: 46px !important;
}

html[data-theme="dark"] button p,
html[data-theme="dark"] button span,
html[data-theme="dark"] button div,
html[data-theme="dark"] .stButton > button p,
html[data-theme="dark"] .stButton > button span,
html[data-theme="dark"] .stButton > button div,
:root:not([data-theme="light"]) button p,
:root:not([data-theme="light"]) .stButton > button p {
    color: #F8FAFC !important;
    font-weight: 800 !important;
}

html[data-theme="dark"] button:hover,
html[data-theme="dark"] .stButton > button:hover,
:root:not([data-theme="light"]) button:hover {
    border-color: #38BDF8 !important;
    color: #38BDF8 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 0 #0369A1, 0 6px 14px rgba(14, 165, 233, 0.4) !important;
}

html[data-theme="dark"] button:hover p,
html[data-theme="dark"] button:hover span,
html[data-theme="dark"] .stButton > button:hover p,
html[data-theme="dark"] .stButton > button:hover span,
:root:not([data-theme="light"]) button:hover p {
    color: #38BDF8 !important;
}

/* Ô CỜ 15-PUZZLE (4x4 GRID) TRONG DARK THEME */
html[data-theme="dark"] div[data-testid="stColumn"] div[data-testid="stColumn"] .stButton > button,
html[data-theme="dark"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] .stButton > button,
:root:not([data-theme="light"]) div[data-testid="stColumn"] div[data-testid="stColumn"] .stButton > button,
:root:not([data-theme="light"]) [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] .stButton > button {
    height: 68px !important;
    font-size: 1.65rem !important;
    font-weight: 900 !important;
    border: 2.5px solid #475569 !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 0 #0F172A, 0 6px 14px rgba(0, 0, 0, 0.45) !important;
}

html[data-theme="dark"] div[data-testid="stColumn"] div[data-testid="stColumn"] .stButton > button p,
html[data-theme="dark"] [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] .stButton > button p,
:root:not([data-theme="light"]) div[data-testid="stColumn"] div[data-testid="stColumn"] .stButton > button p,
:root:not([data-theme="light"]) [data-testid="stHorizontalBlock"] [data-testid="stHorizontalBlock"] .stButton > button p {
    font-size: 1.65rem !important;
    font-weight: 900 !important;
    color: #F8FAFC !important;
}

/* Ô CÓ THỂ DI CHUYỂN (Primary - Xanh cyan sáng) */
html[data-theme="dark"] button[kind="primary"],
html[data-theme="dark"] button[data-testid*="primary"],
html[data-theme="dark"] .stButton > button[kind="primary"],
:root:not([data-theme="light"]) button[kind="primary"],
:root:not([data-theme="light"]) .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%) !important;
    background-color: #0EA5E9 !important;
    color: #FFFFFF !important;
    border: 2.5px solid #38BDF8 !important;
    box-shadow: 0 4px 0 #0369A1, 0 6px 20px rgba(14, 165, 233, 0.6) !important;
    height: 68px !important;
    cursor: pointer !important;
}

html[data-theme="dark"] button[kind="primary"] p,
html[data-theme="dark"] button[kind="primary"] span,
html[data-theme="dark"] button[kind="primary"] div,
:root:not([data-theme="light"]) button[kind="primary"] p {
    color: #FFFFFF !important;
    font-weight: 900 !important;
}

html[data-theme="dark"] button[kind="primary"]:hover,
:root:not([data-theme="light"]) button[kind="primary"]:hover {
    filter: brightness(1.15);
    transform: translateY(-2px) !important;
}

/* Ô TRỐNG (Disabled) */
html[data-theme="dark"] button:disabled,
html[data-theme="dark"] .stButton > button:disabled,
:root:not([data-theme="light"]) button:disabled,
:root:not([data-theme="light"]) .stButton > button:disabled {
    background: #0B0F19 !important;
    background-color: #0B0F19 !important;
    border: 2.5px dashed #334155 !important;
    box-shadow: inset 0 3px 8px rgba(0, 0, 0, 0.6) !important;
    opacity: 0.95 !important;
    cursor: default !important;
}

/* THẺ THỐNG SỐ (METRIC) TRONG DARK THEME */
html[data-theme="dark"] [data-testid="stMetric"],
:root:not([data-theme="light"]) [data-testid="stMetric"] {
    background-color: #1E293B !important;
    border: 2px solid #334155 !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45) !important;
}

html[data-theme="dark"] [data-testid="stMetricLabel"] p,
html[data-theme="dark"] [data-testid="stMetricLabel"] div,
:root:not([data-theme="light"]) [data-testid="stMetricLabel"] p {
    color: #94A3B8 !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

html[data-theme="dark"] [data-testid="stMetricValue"] div,
:root:not([data-theme="light"]) [data-testid="stMetricValue"] div {
    color: #F8FAFC !important;
    font-size: 2.1rem !important;
    font-weight: 900 !important;
}

/* ALERT & CONTAINERS TRONG DARK THEME */
html[data-theme="dark"] [data-testid="stAlert"],
:root:not([data-theme="light"]) [data-testid="stAlert"] {
    background-color: #172554 !important;
    border: 2px solid #1D4ED8 !important;
    color: #DBEAFE !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

html[data-theme="dark"] [data-testid="stExpander"],
html[data-theme="dark"] div[data-testid="stVerticalBlockBorderWrapper"],
:root:not([data-theme="light"]) [data-testid="stExpander"] {
    background-color: #1E293B !important;
    border: 2px solid #334155 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45) !important;
}

html[data-theme="dark"] [data-testid="stExpander"] summary,
:root:not([data-theme="light"]) [data-testid="stExpander"] summary {
    font-weight: 700 !important;
    color: #F8FAFC !important;
}

html[data-theme="dark"] [data-baseweb="textarea"],
:root:not([data-theme="light"]) [data-baseweb="textarea"] {
    background-color: #0B0F19 !important;
    border: 2px solid #334155 !important;
    border-radius: 10px !important;
    color: #F8FAFC !important;
}

html[data-theme="dark"] [data-baseweb="textarea"] textarea,
:root:not([data-theme="light"]) [data-baseweb="textarea"] textarea {
    color: #F8FAFC !important;
    font-weight: 600 !important;
}

/* ==========================================================================
   6. BẢNG XẾP HẠNG TOP 10 (LEADERBOARD HTML TABLE)
   ========================================================================== */
.leaderboard-card {
    border-radius: 14px;
    overflow: hidden;
    margin-top: 8px;
    margin-bottom: 12px;
}

.leaderboard-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.93rem;
    text-align: left;
}

/* Light Mode Leaderboard */
html[data-theme="light"] .leaderboard-card {
    border: 2px solid #CBD5E1;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
}
html[data-theme="light"] .leaderboard-table {
    background: #FFFFFF;
}
html[data-theme="light"] .leaderboard-table th {
    background: #F1F5F9;
    color: #334155;
    font-weight: 800;
    padding: 11px 14px;
    border-bottom: 2px solid #CBD5E1;
    text-transform: uppercase;
    font-size: 0.82rem;
    letter-spacing: 0.04em;
}
html[data-theme="light"] .leaderboard-table td {
    padding: 10px 14px;
    color: #0F172A;
    border-bottom: 1px solid #E2E8F0;
    font-weight: 600;
}
html[data-theme="light"] .leaderboard-table tr:last-child td {
    border-bottom: none;
}
html[data-theme="light"] .leaderboard-table tr:hover td {
    background: #F8FAFC;
}
html[data-theme="light"] .badge-steps {
    display: inline-block;
    padding: 2px 10px;
    background: #E0F2FE;
    color: #0369A1;
    border-radius: 20px;
    font-weight: 800;
    font-size: 0.88rem;
}

/* Dark Mode Leaderboard */
html[data-theme="dark"] .leaderboard-card,
:root:not([data-theme="light"]) .leaderboard-card {
    border: 2px solid #334155;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45);
}
html[data-theme="dark"] .leaderboard-table,
:root:not([data-theme="light"]) .leaderboard-table {
    background: #1E293B;
}
html[data-theme="dark"] .leaderboard-table th,
:root:not([data-theme="light"]) .leaderboard-table th {
    background: #0F172A;
    color: #94A3B8;
    font-weight: 800;
    padding: 11px 14px;
    border-bottom: 2px solid #334155;
    text-transform: uppercase;
    font-size: 0.82rem;
    letter-spacing: 0.04em;
}
html[data-theme="dark"] .leaderboard-table td,
:root:not([data-theme="light"]) .leaderboard-table td {
    padding: 10px 14px;
    color: #F8FAFC;
    border-bottom: 1px solid #334155;
    font-weight: 600;
}
html[data-theme="dark"] .leaderboard-table tr:last-child td,
:root:not([data-theme="light"]) .leaderboard-table tr:last-child td {
    border-bottom: none;
}
html[data-theme="dark"] .leaderboard-table tr:hover td,
:root:not([data-theme="light"]) .leaderboard-table tr:hover td {
    background: #273549;
}
html[data-theme="dark"] .badge-steps,
:root:not([data-theme="light"]) .badge-steps {
    display: inline-block;
    padding: 2px 10px;
    background: #0369A1;
    color: #F0F9FF;
    border-radius: 20px;
    font-weight: 800;
    font-size: 0.88rem;
}

/* ==========================================================================
   7. THEME TOGGLE BUTTON UI (Top-Right Header)
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
    border: 2px solid #94A3B8;
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
"""

THEME_JS = """
<script>
(function() {
    const doc = window.parent.document;
    const win = window.parent;

    if (!doc || !win) return;

    // 1. Cập nhật Icon nút Toggle
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

    // 2. Áp dụng theme vào DOM
    win.__stApplyThemeToDOM = function(theme) {
        doc.documentElement.setAttribute('data-theme', theme);
        if (doc.body) {
            doc.body.setAttribute('data-theme', theme);
        }
        const appContainer = doc.querySelector('.stApp');
        if (appContainer) {
            appContainer.setAttribute('data-theme', theme);
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
                overlay.style.backgroundColor = nextTheme === 'dark' ? '#0B0F19' : '#F8FAFC';
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

        let savedTheme = 'light';
        try {
            const search = win.location.search;
            if (search.includes('theme=dark')) {
                savedTheme = 'dark';
            } else if (search.includes('theme=light')) {
                savedTheme = 'light';
            } else {
                savedTheme = win.localStorage.getItem('st_theme_mode') || 'light';
            }
        } catch (e) {
            savedTheme = 'light';
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
    Tiêm hệ thống Theme Light/Dark và Nút Toggle với hiệu ứng Circular Reveal vào Streamlit.
    """
    st.html(f"<style id=\"st-theme-system-css\">{THEME_CSS}</style>")
    components.html(THEME_JS, height=0, width=0)
