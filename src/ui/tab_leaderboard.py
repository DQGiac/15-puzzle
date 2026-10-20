"""
Tab Bảng Xếp Hạng Top 10 và Quản lý Lưu trữ Dữ liệu (Storage).
Bao gồm:
    - Bảng xếp hạng Top 10 người chơi giải nhanh nhất (ít bước nhất, thời gian ngắn nhất).
    - Lưu và tải lại ván chơi (Save/Load state vào data/save.dat).
    - Chức năng dọn sạch hoặc khôi phục dữ liệu database.
"""

import streamlit as st
from src.logic.engine import GameEngine
from src.models.record import ScoreRecord
from src.ui.tab_puzzle import init_session_state
from src.storage.storage import (
    load_leaderboard,
    save_leaderboard,
    save_game,
    load_game,
    DEFAULT_SAVE_FILE,
    DEFAULT_LEADERBOARD_FILE,
)


def render_tab_leaderboard():
    """Hiển thị màn hình Bảng Xếp Hạng và Quản lý Lưu Trữ."""
    init_session_state()
    st.subheader("🏆 Bảng Xếp Hạng Top 10 & Quản Lý Dữ Liệu", divider="rainbow")

    col_lead, col_save = st.columns([1.25, 1], gap="large")

    # -------------------------------------------------------------------------
    # CỘT TRÁI: BẢNG XẾP HẠNG TOP 10
    # -------------------------------------------------------------------------
    with col_lead:
        st.write("### 🥇 Top 10 Kỷ Lục Người Chơi")
        st.caption(f"Dữ liệu được lưu trữ tự động tại `{DEFAULT_LEADERBOARD_FILE.name}`:")

        records = load_leaderboard()

        if records:
            medals = ["🥇 Hạng 1", "🥈 Hạng 2", "🥉 Hạng 3"]
            rows_html = ""
            for i, rec in enumerate(records[:10]):
                rank_str = medals[i] if i < 3 else f"#{i+1}"
                row_cls = f"rank-{i+1}" if i < 3 else ""
                rows_html += f"""
                <tr class="{row_cls}">
                    <td style="font-weight: 800;">{rank_str}</td>
                    <td><strong style="color: #FFFFFF;">{rec.player_name}</strong></td>
                    <td><span class="badge-steps">{rec.step_count}</span></td>
                    <td><span style="color: #A6E3A1; font-weight: 800; font-family: monospace;">{rec.elapsed_time:.1f}s</span></td>
                    <td style="opacity: 0.75; font-size: 0.85rem; font-family: monospace;">{rec.date_played}</td>
                </tr>
                """

            table_html = f"""
            <div class="leaderboard-card">
                <table class="leaderboard-table">
                    <thead>
                        <tr>
                            <th style="width: 20%;">Thứ hạng</th>
                            <th style="width: 30%;">Người chơi</th>
                            <th style="width: 18%;">Số bước</th>
                            <th style="width: 16%;">Thời gian</th>
                            <th style="width: 16%;">Ngày</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
            """
            st.html(table_html)
        else:
            st.info("Chưa có thành tích nào trong bảng xếp hạng. Hãy chơi và ghi danh kỷ lục đầu tiên!")

        st.write("")
        c_clear, c_refresh = st.columns(2, gap="small")
        with c_clear:
            if st.button("🗑️ Dọn Sạch Bảng Xếp Hạng", use_container_width=True):
                save_leaderboard([], DEFAULT_LEADERBOARD_FILE)
                st.toast("Đã dọn sạch bảng xếp hạng!", icon="🗑️")
                st.rerun()
        with c_refresh:
            if st.button("🔄 Nạp Dữ Liệu Mẫu Chuẩn", use_container_width=True):
                default_records = [
                    ScoreRecord("Player Pro", 28, 14.50),
                    ScoreRecord("AI (IDA*)", 32, 0.12),
                    ScoreRecord("Player 1", 45, 22.30),
                    ScoreRecord("Player 2", 54, 31.80),
                    ScoreRecord("Champion", 62, 45.20),
                ]
                save_leaderboard(default_records, DEFAULT_LEADERBOARD_FILE)
                st.toast("Đã khôi phục dữ liệu mẫu bảng xếp hạng!", icon="🔄")
                st.rerun()

    # -------------------------------------------------------------------------
    # CỘT PHẢI: QUẢN LÝ LƯU TRỮ VÁN ĐẤU (SAVE / LOAD GAME)
    # -------------------------------------------------------------------------
    with col_save:
        st.write("### 💾 Quản Lý Lưu Trữ Ván Chơi")
        st.caption(f"Lưu trạng thái snapshot bàn cờ vào `{DEFAULT_SAVE_FILE.name}`:")

        engine: GameEngine = st.session_state.game_engine

        with st.container(border=True):
            st.write("#### 🎮 Trạng thái snapshot bàn cờ:")
            status_chips_html = f"""
            <div class="bench-stats-grid">
                <div class="bench-stat-chip">
                    <span class="chip-label">Số bước đi</span>
                    <span class="chip-val">{engine.board_state.step_count}</span>
                </div>
                <div class="bench-stat-chip">
                    <span class="chip-label">Thời gian</span>
                    <span class="chip-val">{engine.board_state.elapsed_time:.1f}s</span>
                </div>
                <div class="bench-stat-chip">
                    <span class="chip-label">Ô trống (r, c)</span>
                    <span class="chip-val">[{engine.board_state.empty_pos[0]}, {engine.board_state.empty_pos[1]}]</span>
                </div>
            </div>
            """
            st.markdown(status_chips_html, unsafe_allow_html=True)

            c_save, c_load = st.columns(2, gap="small")
            with c_save:
                if st.button("💾 Lưu Ván Game", type="primary", use_container_width=True):
                    if save_game(engine.board_state):
                        st.toast("Đã lưu trạng thái ván game vào data/save.dat!", icon="💾")
                        st.success("Lưu game thành công!")
                    else:
                        st.error("Không thể lưu game.")

            with c_load:
                if st.button("📂 Tải Lại Game", use_container_width=True):
                    loaded = load_game()
                    if loaded:
                        engine.board_state = loaded
                        engine.history.clear()
                        st.session_state.timer_running = False
                        st.session_state.accumulated_time = loaded.elapsed_time
                        st.session_state.ai_solution = None
                        st.session_state.ai_step_idx = 0
                        st.session_state.won_notified = False
                        st.toast("Đã tải lại ván game từ data/save.dat!", icon="📂")
                        st.success("Tải game thành công!")
                        st.rerun()
                    else:
                        st.warning("Chưa có file lưu hoặc dữ liệu file không hợp lệ.")
