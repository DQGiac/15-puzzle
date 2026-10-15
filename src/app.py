import html
import streamlit as st

# 1. Cấu hình trang (bắt buộc đầu file)
st.set_page_config(
    page_title="15-Puzzle",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Bộ mã CSS tùy biến (Dark Slate / Blue Theme tương tự bản gốc)
_BASE_CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

:root { color-scheme: dark; }
.stApp {
    background: #1a202c;
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}
[data-testid="stHeader"] { background: rgba(26, 32, 44, 0); }
[data-testid="stToolbar"], #MainMenu, footer { visibility: hidden; }
[data-testid="stMainBlockContainer"] {
    max-width: 850px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
}
.puzzle-title {
    text-align: center;
    font-family: 'Inter', sans-serif;
    font-size: 2.5rem;
    line-height: 1.15;
    font-weight: 800;
    margin: 0 0 1.5rem 0;
    background: linear-gradient(90deg, #63b3ed, #68d391);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Khung bàn cờ */
.st-key-board_shell {
    width: 320px;
    max-width: 100%;
    margin: 0 auto;
    padding: 10px;
    background: #2d3748;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,.5);
}
.st-key-board_shell [data-testid="HorizontalBlock"],
.st-key-board_shell [data-testid="stHorizontalBlock"],
.st-key-board_shell [data-testid="stVerticalBlock"] {
    gap: 5px !important;
}
.st-key-board_shell [data-testid="stElementContainer"] {
    margin-bottom: 0 !important;
}
.st-key-board_shell [data-testid="column"] {
    min-width: 0 !important;
}
.st-key-board_shell .stButton { width: 100%; }
.st-key-board_shell .stButton > button {
    box-sizing: border-box !important;
    width: 100% !important;
    min-width: 0 !important;
    height: 70px !important;
    min-height: 70px !important;
    padding: 0 !important;
    border: 2px solid #2b6cb0 !important;
    border-radius: 8px !important;
    background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
    color: #fff !important;
    box-shadow: 0 4px 6px rgba(0,0,0,.3);
    font-size: 1.75rem !important;
    font-weight: 800 !important;
    line-height: 1 !important;
    transition: filter .15s ease-in-out, transform .15s ease-in-out;
}
.st-key-board_shell .stButton > button:hover {
    filter: brightness(1.1);
    border-color: #2b6cb0 !important;
}
.st-key-board_shell .stButton > button:focus:not(:active) {
    box-shadow: 0 0 0 2px rgba(99,179,237,.35), 0 4px 6px rgba(0,0,0,.3) !important;
}
.st-key-board_shell .empty-tile {
    width: 100%;
    height: 70px;
    background: transparent;
    border: 0;
}

/* Khung hiển thị thông số Moves & Time */
.st-key-stats_panel {
    width: 320px;
    max-width: 100%;
    box-sizing: border-box;
    margin: 16px auto 0 auto;
    padding: 11px 13px;
    border: 1px solid #374151;
    border-radius: 8px;
    background: #1f2937;
}
.st-key-stats_panel [data-testid="stHorizontalBlock"] { gap: 6px !important; }
.stat-label { font-size: 1rem; color: #e2e8f0; white-space: nowrap; }
.stat-number { font-weight: 800; }
.stat-moves { color: #63b3ed; }
.stat-time { color: #68d391; }

.ai-status {
    width: 320px;
    max-width: 100%;
    min-height: 23px;
    margin: 7px auto 0 auto;
    text-align: center;
    font-size: .85rem;
    color: #f6e05e;
}
.ai-status.error { color: #fc8181; }
.ai-status.success { color: #68d391; }

/* Cột phải: Khối điều khiển và Bảng xếp hạng */
.st-key-controls_panel, .st-key-leaderboard_panel {
    width: 100%;
    max-width: 350px;
    box-sizing: border-box;
    margin: 0 auto 16px auto;
    padding: 20px;
    background: #2d3748;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,.3);
}
.panel-heading {
    color: #f7fafc;
    font-size: 1.25rem;
    font-weight: 800;
    margin: 0 0 13px 0;
    padding-bottom: 9px;
    border-bottom: 1px solid #4a5568;
}
.difficulty-label {
    color: #a0aec0;
    font-size: .9rem;
    font-weight: 600;
    margin: 14px 0 7px 0;
}
.stButton > button {
    background: #4a5568 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 6px !important;
    padding: .5rem .65rem !important;
    min-height: 38px;
    font-family: 'Inter', sans-serif;
    font-weight: 600 !important;
    transition: background-color .2s ease;
}
.stButton > button:hover { background: #718096 !important; }
.st-key-btn_solve button {
    background: #48bb78 !important;
}
.st-key-btn_solve button:hover { background: #38a169 !important; }
.st-key-diff_10 button, .st-key-diff_30 button, .st-key-diff_50 button {
    background: #2563eb !important;
}
.st-key-diff_10 button:hover, .st-key-diff_30 button:hover, .st-key-diff_50 button:hover {
    background: #3b82f6 !important;
}
.st-key-diff_50 button {
    background: #60a5fa !important;
}

/* Bảng xếp hạng Top 10 */
.leaderboard-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
    font-size: 13px;
    table-layout: fixed;
}
.leaderboard-table th, .leaderboard-table td {
    padding: 8px 4px;
    text-align: left;
    border-bottom: 1px solid #4a5568;
    overflow-wrap: anywhere;
}
.leaderboard-table th { color: #a0aec0; font-weight: 600; }
.leaderboard-table td { color: #e2e8f0; }
.leaderboard-table td.player-name { color: #fff; font-weight: 600; }
.empty-leaderboard { color: #a0aec0; font-size: .9rem; padding: 10px 0; }
"""

st.markdown(f"<style>{_BASE_CSS}</style>", unsafe_allow_html=True)

# 3. Tiêu đề ứng dụng
st.markdown('<h1 class="puzzle-title">15-Puzzle</h1>', unsafe_allow_html=True)

# 4. Phân chia 2 cột lớn
board_col, controls_col = st.columns([1.05, 1], gap="large", vertical_alignment="top")

# --- CỘT TRÁI: BÀN CỜ 4x4 & THỐNG SỐ ---
with board_col:
    # Lưới bàn cờ 4x4
    with st.container(key="board_shell"):
        # Trạng thái tĩnh hoàn chỉnh: số 1 -> 15, số 0 là ô trống góc cuối
        board_data = list(range(1, 16)) + [0]
        SIZE = 4
        for row in range(SIZE):
            cells = st.columns(4, gap="small")
            for col in range(SIZE):
                index = row * SIZE + col
                val = board_data[index]
                with cells[col]:
                    if val == 0:
                        st.markdown('<div class="empty-tile"></div>', unsafe_allow_html=True)
                    else:
                        st.button(str(val), key=f"tile_{index}", use_container_width=True)

    # Khung thống số Moves & Time
    with st.container(key="stats_panel"):
        left, right = st.columns(2, gap="small")
        left.markdown(
            '<div class="stat-label">Moves: <span class="stat-number stat-moves">0</span></div>',
            unsafe_allow_html=True,
        )
        right.markdown(
            '<div class="stat-label">Time: <span class="stat-number stat-time">0.0s</span></div>',
            unsafe_allow_html=True,
        )

    # Thông báo trạng thái
    st.markdown('<div class="ai-status">Ready to play</div>', unsafe_allow_html=True)

# --- CỘT PHẢI: BẢNG ĐIỀU KHIỂN & BẢNG XẾP HẠNG ---
with controls_col:
    # Thẻ điều khiển Controls
    with st.container(key="controls_panel"):
        st.markdown('<div class="panel-heading">Controls</div>', unsafe_allow_html=True)
        control_a, control_b = st.columns(2, gap="small")
        with control_a:
            st.button("🔄 Shuffle (R)", key="btn_shuffle", use_container_width=True)
        with control_b:
            st.button("⚡ Auto Solve", key="btn_solve", use_container_width=True)
        with control_a:
            st.button("💾 Save (S)", key="btn_save", use_container_width=True)
        with control_b:
            st.button("📂 Load (L)", key="btn_load", use_container_width=True)

        st.markdown('<div class="difficulty-label">Difficulty (Scramble Steps)</div>', unsafe_allow_html=True)
        diff_cols = st.columns(3, gap="small")
        difficulty_options = [(10, "Easy (1)"), (30, "Med (2)"), (50, "Hard (3)")]
        for col, (steps, label) in zip(diff_cols, difficulty_options):
            with col:
                st.button(label, key=f"diff_{steps}", use_container_width=True)

    # Thẻ Top 10 Leaderboard
    with st.container(key="leaderboard_panel"):
        st.markdown('<div class="panel-heading">🏆 Top 10</div>', unsafe_allow_html=True)
        mock_scores = [
            {"rank": "🥇", "name": "Antigravity", "moves": 38, "time": "15.2s"},
            {"rank": "🥈", "name": "Player 1", "moves": 45, "time": "18.0s"},
            {"rank": "🥉", "name": "Player 2", "moves": 58, "time": "23.6s"},
        ]
        rows = "".join([
            f"<tr><td>{s['rank']}</td><td class=\"player-name\">{html.escape(s['name'])}</td><td>{s['moves']}</td><td>{s['time']}</td></tr>"
            for s in mock_scores
        ])
        table_html = f"""
        <table class="leaderboard-table">
            <thead>
                <tr>
                    <th style="width:17%">Rank</th>
                    <th style="width:37%">Name</th>
                    <th style="width:22%">Moves</th>
                    <th style="width:24%">Time</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        """
        st.markdown(table_html, unsafe_allow_html=True)
