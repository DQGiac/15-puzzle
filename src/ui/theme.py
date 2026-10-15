"""
Module quản lý hệ thống Theme (Light/Dark) với hiệu ứng Circular Reveal Animation.
Tự động tích hợp vào Streamlit app mà không ảnh hưởng đến chức năng hiện có.
"""
import streamlit as st
import streamlit.components.v1 as components

# Mã CSS định nghĩa toàn bộ Design System cho Light & Dark theme
THEME_CSS = """
<style id="st-theme-system-css">
/* ==========================================================================
   DESIGN TOKENS & CSS VARIABLES
   ========================================================================== */
:root,
html[data-theme="dark"],
.stApp[data-theme="dark"] {
    --bg-main: #0B0F19;
    --bg-sidebar: #111827;
    --bg-card: #1E293B;
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --border-color: #334155;
    --accent-primary: #10B981;
    --accent-hover: #34D399;
    --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    --tile-bg: #1E293B;
    --tile-border: #334155;
    --tile-text: #F8FAFC;
}

html[data-theme="light"],
.stApp[data-theme="light"] {
    --bg-main: #F8FAFC;
    --bg-sidebar: #F1F5F9;
    --bg-card: #FFFFFF;
    --text-primary: #0F172A;
    --text-secondary: #64748B;
    --border-color: #E2E8F0;
    --accent-primary: #10B981;
    --accent-hover: #059669;
    --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    --tile-bg: #FFFFFF;
    --tile-border: #CBD5E1;
    --tile-text: #0F172A;
}

/* ==========================================================================
   VIEW TRANSITIONS API: CIRCULAR REVEAL ANIMATION
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

/* Fallback circular reveal overlay */
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
   GLOBAL APP THEMING
   ========================================================================== */
html, body {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
    transition: background-color 0.25s ease, color 0.25s ease;
}

.stApp,
[data-testid="stAppViewContainer"],
.main {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
}

[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* Sidebar */
[data-testid="stSidebar"],
section[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-color) !important;
}

/* Typography, Headings & Text */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
}

p, span, label {
    color: inherit;
}

/* Form Labels & Captions */
html[data-theme="light"] [data-testid="stWidgetLabel"] label,
html[data-theme="light"] [data-testid="stWidgetLabel"] p,
html[data-theme="light"] .stWidgetLabel p,
html[data-theme="light"] .stMarkdown p {
    color: #0F172A !important;
}

html[data-theme="light"] .stCaption,
html[data-theme="light"] [data-testid="stCaptionContainer"] p,
html[data-theme="light"] small {
    color: #64748B !important;
}

html[data-theme="dark"] [data-testid="stWidgetLabel"] label,
html[data-theme="dark"] [data-testid="stWidgetLabel"] p,
html[data-theme="dark"] .stWidgetLabel p,
html[data-theme="dark"] .stMarkdown p {
    color: #F8FAFC !important;
}

html[data-theme="dark"] .stCaption,
html[data-theme="dark"] [data-testid="stCaptionContainer"] p,
html[data-theme="dark"] small {
    color: #94A3B8 !important;
}

/* Cards, Metric Containers */
[data-testid="stMetric"],
div[data-testid="stMetric"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    box-shadow: var(--card-shadow) !important;
}
[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] div {
    color: var(--text-secondary) !important;
}
[data-testid="stMetricValue"] div {
    color: var(--text-primary) !important;
}

/* Borders & Dividers */
hr {
    border-color: var(--border-color) !important;
}

/* Native buttons */
.stButton > button {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    border-color: var(--accent-primary) !important;
    color: var(--accent-primary) !important;
    background-color: var(--bg-card) !important;
    transform: translateY(-1px);
}
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background-color: var(--accent-primary) !important;
    color: #FFFFFF !important;
    border: none !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
    background-color: var(--accent-hover) !important;
    color: #FFFFFF !important;
}

/* 15-Puzzle tile buttons */
.stButton > button:disabled {
    background-color: transparent !important;
    border: 1px dashed var(--border-color) !important;
    opacity: 0.3 !important;
}

/* Inputs, Selectboxes, Dropdowns */
[data-baseweb="input"],
[data-baseweb="select"] > div,
.stSelectbox > div > div {
    background-color: var(--bg-card) !important;
    border-color: var(--border-color) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}
[data-baseweb="input"] input,
[data-baseweb="select"] span,
[data-baseweb="select"] div {
    color: var(--text-primary) !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"],
ul[role="listbox"] {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
}
li[role="option"] {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
}
li[role="option"]:hover {
    background-color: var(--bg-sidebar) !important;
    color: var(--accent-primary) !important;
}

/* Radio buttons & Sliders */
[data-testid="stRadio"] label span,
[data-testid="stRadio"] div[role="radiogroup"] label {
    color: var(--text-primary) !important;
}
[data-testid="stSlider"] label p,
[data-testid="stSlider"] div {
    color: var(--text-primary) !important;
}

/* Dataframe & Tables */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
}
html[data-theme="light"] [data-testid="stDataFrame"] {
    filter: invert(0.92) hue-rotate(180deg);
}

/* Tabs */
[data-baseweb="tab-list"] {
    border-bottom: 1px solid var(--border-color) !important;
    background-color: transparent !important;
}
[data-baseweb="tab"] {
    color: var(--text-secondary) !important;
}
[data-baseweb="tab"] p,
[data-baseweb="tab"] span {
    color: var(--text-secondary) !important;
}
[data-baseweb="tab"][aria-selected="true"] {
    color: var(--accent-primary) !important;
    border-bottom-color: var(--accent-primary) !important;
}
[data-baseweb="tab"][aria-selected="true"] p,
[data-baseweb="tab"][aria-selected="true"] span {
    color: var(--accent-primary) !important;
    font-weight: 600;
}

/* Alerts / Info */
[data-testid="stAlert"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
}

/* ==========================================================================
   THEME TOGGLE BUTTON UI (Top-Right Header)
   ========================================================================== */
#theme-toggle-root {
    position: fixed;
    top: 10px;
    right: 175px;
    z-index: 999999;
    display: flex;
    align-items: center;
    justify-content: center;
}

@media (max-width: 768px) {
    #theme-toggle-root {
        top: 10px;
        right: 56px;
    }
}

.theme-toggle-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    box-shadow: var(--card-shadow);
    color: var(--text-primary);
    cursor: pointer;
    outline: none;
    padding: 0;
    transition: transform 0.25s cubic-bezier(0.22, 1, 0.36, 1),
                border-color 0.25s ease,
                background-color 0.25s ease,
                box-shadow 0.25s ease;
}

.theme-toggle-btn:hover {
    transform: scale(1.1);
    border-color: var(--accent-primary);
    box-shadow: 0 0 12px rgba(16, 185, 129, 0.35);
}

.theme-toggle-btn:active {
    transform: scale(0.95);
}

.theme-toggle-icon {
    width: 20px;
    height: 20px;
    transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.2s ease;
}

.theme-toggle-btn:hover .theme-toggle-icon {
    transform: rotate(20deg);
}
</style>
"""

# Mã JavaScript tiêm và thực thi hiệu ứng Circular Reveal Animation
THEME_JS = """
<script>
(function() {
    const doc = window.parent.document;
    const win = window.parent;

    if (!doc || !win) return;

    // 1. Kiểm tra và tiêm CSS vào parent document head nếu chưa có hoặc cập nhật
    let styleTag = doc.getElementById('st-theme-system-css');
    if (!styleTag) {
        styleTag = doc.createElement('style');
        styleTag.id = 'st-theme-system-css';
        styleTag.textContent = `__THEME_CSS_CONTENT__`;
        doc.head.appendChild(styleTag);
    } else {
        styleTag.textContent = `__THEME_CSS_CONTENT__`;
    }

    // 2. Định nghĩa hàm cập nhật giao diện nút bấm trên window.parent
    win.__stUpdateButtonUI = function(theme) {
        const btn = doc.getElementById('theme-toggle-btn');
        if (!btn) return;
        
        // In dark mode -> Sun icon (☀️)
        // In light mode -> Moon icon (🌙)
        if (theme === 'dark') {
            btn.innerHTML = `
                <svg class="theme-toggle-icon" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
            btn.setAttribute('title', 'Switch to Light Mode');
            btn.setAttribute('aria-label', 'Switch to Light Mode');
        } else {
            btn.innerHTML = `
                <svg class="theme-toggle-icon" viewBox="0 0 24 24" fill="none" stroke="#4F46E5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
            `;
            btn.setAttribute('title', 'Switch to Dark Mode');
            btn.setAttribute('aria-label', 'Switch to Dark Mode');
        }
    };

    // 3. Định nghĩa hàm áp dụng theme vào DOM trên window.parent
    win.__stApplyThemeToDOM = function(theme) {
        doc.documentElement.setAttribute('data-theme', theme);
        const appContainer = doc.querySelector('.stApp');
        if (appContainer) {
            appContainer.setAttribute('data-theme', theme);
        }
        try {
            win.localStorage.setItem('st_theme_mode', theme);
        } catch (e) {}
        win.__stUpdateButtonUI(theme);
    };

    // 4. Hiệu ứng Circular Reveal Animation cốt lõi trên window.parent
    win.__stTriggerCircularReveal = function(event) {
        try {
            let currentTheme = 'dark';
            try {
                currentTheme = win.localStorage.getItem('st_theme_mode') || 'dark';
            } catch (e) {}

            const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
            const btn = doc.getElementById('theme-toggle-btn');
            
            // Lấy tọa độ tâm nút bấm làm điểm xuất phát hình tròn
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

            // Tính bán kính lớn nhất để phủ kín toàn bộ 4 góc màn hình từ vị trí nút bấm
            const endRadius = Math.hypot(
                Math.max(x, win.innerWidth - x),
                Math.max(y, win.innerHeight - y)
            );

            // Kiểm tra prefers-reduced-motion
            const prefersReducedMotion = win.matchMedia && win.matchMedia('(prefers-reduced-motion: reduce)').matches;
            if (prefersReducedMotion) {
                win.__stApplyThemeToDOM(nextTheme);
                return;
            }

            // Cách 1: Native View Transitions API
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
                // Cách 2: Fallback Radial Overlay cho trình duyệt chưa hỗ trợ View Transitions
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

    // 5. Khởi tạo nút Toggle trên Header và bind sự kiện
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
            savedTheme = win.localStorage.getItem('st_theme_mode') || 'dark';
        } catch (e) {}

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
    Hàm này được gọi 1 lần tại đầu trang chính của Streamlit.
    """
    # 1. Tiêm CSS thông qua st.markdown
    clean_css = THEME_CSS.replace("<style id=\"st-theme-system-css\">", "").replace("</style>", "")
    st.markdown(f"<style id=\"st-theme-system-css\">{clean_css}</style>", unsafe_allow_html=True)

    # 2. Tiêm JS khởi tạo và nút toggle với startViewTransition qua iframe component
    js_payload = THEME_JS.replace("__THEME_CSS_CONTENT__", clean_css.replace("\n", " ").replace("\"", "'"))
    components.html(js_payload, height=0, width=0)
