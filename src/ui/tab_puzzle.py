"""
Giao diện Trò chơi 15-Puzzle (Lưới 4x4 tương tác, AI Solver, Save/Load, Leaderboard).

Tính năng:
    - Bàn cờ 4x4 tương tác: click vào ô kề ô trống để trượt ô.
    - Bộ đếm số bước (Moves) và thời gian thực (Time).
    - Các nút điều khiển: Shuffle (R), Auto Solve (Space), Save (S), Load (L).
    - Chọn độ khó: Easy (10 bước), Med (30 bước), Hard (50 bước).
    - AI Solver tự động: Giải bằng thuật toán IDA* (Heuristic Manhattan f = g + 2*h kết hợp HashTable).
    - Trình diễn lời giải (Step-by-step & Auto Play).
    - Nhập ma trận từ bên ngoài và kiểm tra tính giải được (Solvability Check).
    - Bảng xếp hạng Top 10 (Leaderboard) lưu vào leaderboard.csv.
    - Phím tắt bàn phím: R (Shuffle), S (Save), L (Load), Space (Auto Solve).
"""

import time
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from src.models.board_state import BoardState
from src.models.record import ScoreRecord
from src.logic.engine import GameEngine
from src.logic.validator import parse_and_validate_input
from src.algorithms.ida_solver import IDASolver
try:
    from src.algorithms.a_star_solver import AStarSolver
except ImportError:
    AStarSolver = None

from src.storage.storage import (
    save_game,
    load_game,
    load_leaderboard,
    add_score_record,
)


def apply_direction_move(engine: GameEngine, direction: str) -> bool:
    """Di chuyển ô cờ an toàn theo hướng di chuyển của AI."""
    if hasattr(engine, "move_by_direction"):
        return engine.move_by_direction(direction)
    directions = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
    dr, dc = directions.get(direction.upper(), (0, 0))
    er, ec = engine.board_state.empty_pos
    return engine.move(er + dr, ec + dc)


def init_session_state():
    """Khởi tạo toàn bộ trạng thái trong st.session_state nếu chưa có."""
    if "game_engine" not in st.session_state:
        board = BoardState()
        engine = GameEngine(board)
        engine.reset_and_shuffle(steps=30)
        st.session_state.game_engine = engine

    if "ai_algorithm" not in st.session_state:
        st.session_state.ai_algorithm = "IDA*"

    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False

    if "start_timestamp" not in st.session_state:
        st.session_state.start_timestamp = None

    if "accumulated_time" not in st.session_state:
        st.session_state.accumulated_time = 0.0

    if "difficulty" not in st.session_state:
        st.session_state.difficulty = 30

    if "status_message" not in st.session_state:
        st.session_state.status_message = "Sẵn sàng! Nhấn vào ô sáng màu bên cạnh ô trống để trượt."

    if "ai_solution" not in st.session_state:
        st.session_state.ai_solution = None

    if "ai_step_idx" not in st.session_state:
        st.session_state.ai_step_idx = 0

    if "ai_stats" not in st.session_state:
        st.session_state.ai_stats = None

    if "won_notified" not in st.session_state:
        st.session_state.won_notified = False


def get_current_time() -> float:
    """Tính thời gian ván chơi hiện tại tính theo giây."""
    if st.session_state.timer_running and st.session_state.start_timestamp:
        return st.session_state.accumulated_time + (time.time() - st.session_state.start_timestamp)
    return st.session_state.accumulated_time


def stop_timer() -> float:
    """Freeze the timer and return the final elapsed time."""
    elapsed = get_current_time()
    st.session_state.timer_running = False
    st.session_state.accumulated_time = elapsed
    st.session_state.start_timestamp = None
    return elapsed


@st.fragment(run_every="100ms")
def render_live_time():
    """Refresh the time metric without requiring a board interaction."""
    st.metric(label="Thời gian (Time)", value=f"{get_current_time():.1f}s")


def inject_keyboard_shortcuts():
    """Tiêm script bắt phím tắt (R: Shuffle, S: Save, L: Load, Space: Solve)."""
    js_code = """
    <script>
    (function() {
        const doc = window.parent.document;
        if (!doc) return;

        if (window.__15puzzle_listener_attached) return;
        window.__15puzzle_listener_attached = true;

        doc.addEventListener('keydown', function(e) {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            const key = e.key.toLowerCase();
            if (key === 'r') {
                const btn = doc.getElementById('btn_shuffle');
                if (btn) btn.click();
            } else if (key === 's' && !e.ctrlKey && !e.metaKey) {
                const btn = doc.getElementById('btn_save');
                if (btn) btn.click();
            } else if (key === 'l' && !e.ctrlKey && !e.metaKey) {
                const btn = doc.getElementById('btn_load');
                if (btn) btn.click();
            } else if (e.code === 'Space') {
                e.preventDefault();
                const btn = doc.getElementById('btn_solve');
                if (btn) btn.click();
            }
        });
    })();
    </script>
    """
    components.html(js_code, height=0, width=0)


def render_tab_puzzle():
    """Hàm hiển thị chính của toàn bộ giao diện 15-Puzzle."""
    init_session_state()
    inject_keyboard_shortcuts()

    engine: GameEngine = st.session_state.game_engine
    is_game_won = engine.is_win()

    # Kiểm tra thắng lần đầu để dừng bộ đếm thời gian
    if is_game_won and not st.session_state.won_notified:
        stop_timer()
        st.session_state.won_notified = True
        st.session_state.status_message = "🎉 CHÚC MỪNG! Bạn đã giải thành công 15-Puzzle!"

    elapsed = get_current_time()
    engine.board_state.elapsed_time = elapsed

    # Layout 2 cột: Trái (Bàn cờ & Thống số), Phải (Bảng điều khiển & Leaderboard)
    board_col, controls_col = st.columns([1.18, 1], gap="large")

    # =========================================================================
    # CỘT TRÁI: BÀN CỜ 4x4 & THỐNG SỐ
    # =========================================================================
    with board_col:
        st.subheader("🎮 Bàn cờ 15-Puzzle", divider="rainbow")

        grid = engine.board_state.grid
        size = engine.board_state.size
        valid_moves = set(engine.get_valid_moves())

        # Khung bàn cờ 4x4 dạng khay nổi
        with st.container():
            for r in range(size):
                cells = st.columns(size, gap="small")
                for c in range(size):
                    val = grid[r][c]
                    tile_can_move = (r, c) in valid_moves
                    tile_key = f"tile_{r}_{c}_{val}"

                    with cells[c]:
                        if val == 0:
                            # Ô trống: Disabled, tạo hốc lõm 3D
                            st.button(
                                " ",
                                key=tile_key,
                                disabled=True,
                                use_container_width=True,
                            )
                        else:
                            # Ô số: Nếu có thể di chuyển -> Type Primary (Sáng màu, nổi bật)
                            # Nếu không di chuyển được -> Type Secondary (Màu thẻ sắc nét, viền rõ)
                            btn_clicked = st.button(
                                str(val),
                                key=tile_key,
                                type="primary" if tile_can_move else "secondary",
                                help=f"Nhấn để trượt ô {val} vào ô trống" if tile_can_move else None,
                                # disabled=is_game_won,
                                use_container_width=True,
                            )

                            if btn_clicked and not is_game_won and tile_can_move:
                                if not st.session_state.timer_running:
                                    st.session_state.timer_running = True
                                    st.session_state.start_timestamp = time.time()

                                engine.move(r, c)
                                st.session_state.won_notified = False

                                if engine.is_win():
                                    stop_timer()
                                    st.session_state.won_notified = True
                                    st.session_state.status_message = "🎉 CHÚC MỪNG! Bạn đã hoàn thành xuất sắc!"
                                else:
                                    st.session_state.status_message = f"Đã trượt ô số {val} vào ô trống."
                                st.rerun()

        st.write("")

        # Khung thẻ thống số: Moves, Time, Status
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric(label="Bước đi (Moves)", value=engine.board_state.step_count)
        with m_col2:
            render_live_time()
        m_col3.metric(
            label="Trạng thái (Status)",
            value="🏆 Thắng cuộc!" if is_game_won else ("▶️ Đang chơi" if st.session_state.timer_running else "⏸️ Tạm dừng"),
        )

        st.write("")

        # Thông báo trạng thái
        if is_game_won:
            st.success(st.session_state.status_message)
            st.balloons()
            with st.container(border=True):
                st.write("### 🏅 Ghi danh Bảng Vàng")
                col_name, col_submit = st.columns([2, 1])
                with col_name:
                    player_name = st.text_input("Tên của bạn:", value="Champion", max_chars=20)
                    player_name = player_name.strip().replace(",", "") or "Anonymous"
                with col_submit:
                    st.write("")
                    st.write("")
                    if st.button("💾 Lưu Thành Tích", type="primary", use_container_width=True):
                        rec = ScoreRecord(
                            player_name=player_name.strip() or "Anonymous",
                            step_count=engine.board_state.step_count,
                            elapsed_time=elapsed,
                        )
                        add_score_record(rec)
                        st.toast(f"Đã lưu thành tích của {rec.player_name} vào Top 10!", icon="🏆")
                        st.session_state.won_notified = True
                        st.rerun()
        else:
            st.info(st.session_state.status_message)

        # Trình diễn bước giải của AI nếu đã tìm ra lời giải
        if st.session_state.ai_solution:
            solution = st.session_state.ai_solution
            stats = st.session_state.ai_stats or {}
            st.write("")
            with st.container(border=True):
                algo_used = stats.get("algo", "IDA*")
                st.write(f"### 🤖 Lời giải từ AI ({algo_used})")
                st.caption(
                    f"✨ Tìm thấy lời giải trong **{stats.get('time', 0):.3f}s** | "
                    f"Tổng số bước: **{len(solution)}** | "
                    f"Nút đã duyệt: **{stats.get('nodes', 0)}**"
                )

                curr_idx = st.session_state.ai_step_idx
                step_progress = curr_idx / max(len(solution), 1)
                st.progress(step_progress, text=f"Tiến trình: Bước {curr_idx}/{len(solution)}")

                p_col1, p_col2, p_col3 = st.columns(3)
                with p_col1:
                    if st.button("▶️ Đi 1 bước tiếp", key="btn_next_step", use_container_width=True):
                        if is_game_won:
                            st.toast("Bàn cờ hiện tại đã ở trạng thái giải rồi!", icon="🎯")
                        else:
                            if curr_idx < len(solution):
                                next_move = solution[curr_idx]
                                apply_direction_move(engine, next_move)
                                st.session_state.ai_step_idx += 1
                                st.rerun()
                with p_col2:
                    if st.button("⏩ Giải toàn bộ", key="btn_solve_all", use_container_width=True):
                        if is_game_won:
                            st.toast("Bàn cờ hiện tại đã ở trạng thái giải rồi!", icon="🎯")
                        else:
                            while st.session_state.ai_step_idx < len(solution):
                                next_move = solution[st.session_state.ai_step_idx]
                                apply_direction_move(engine, next_move)
                                st.session_state.ai_step_idx += 1
                            st.session_state.status_message = "🎉 AI đã hoàn thành giải toàn bộ bàn cờ!"
                            st.rerun()
                with p_col3:
                    if st.button("❌ Hủy lời giải", key="btn_cancel_ai", use_container_width=True):
                        st.session_state.ai_solution = None
                        st.session_state.ai_step_idx = 0
                        st.rerun()

                moves_preview = " ➔ ".join(solution[:curr_idx])
                if moves_preview:
                    st.caption(f"**Đã đi:** {moves_preview}")
                remaining = " ➔ ".join(solution[curr_idx:curr_idx + 10])
                if remaining:
                    st.caption(f"**Sắp tới:** {remaining} {'...' if len(solution) > curr_idx + 10 else ''}")

    # =========================================================================
    # CỘT PHẢI: ĐIỀU KHIỂN & BẢNG XẾP HẠNG
    # =========================================================================
    with controls_col:
        st.subheader("⚙️ Điều khiển (Controls)", divider="rainbow")

        # Tùy chọn thuật toán AI
        algo_labels = ["IDA* (Heuristic Manhattan)", "A* (MinHeap Queue)"]
        selected_label = st.radio(
            "Thuật toán AI tự động giải:",
            options=algo_labels,
            index=0,
            horizontal=True,
        )
        print(f"Selected AI Algorithm: {selected_label}")
        st.session_state.ai_algorithm = "IDA*" if "IDA*" in selected_label else "A*"

        # Khung nút điều khiển chính
        ctrl_1, ctrl_2 = st.columns(2, gap="small")
        with ctrl_1:
            shuffle_btn = st.button("🔄 Shuffle (R)", key="btn_shuffle", use_container_width=True)
            save_btn = st.button("💾 Save Game (S)", key="btn_save", use_container_width=True)
        with ctrl_2:
            solve_btn = st.button("⚡ Auto Solve (Space)", key="btn_solve", use_container_width=True)
            load_btn = st.button("📂 Load Game (L)", key="btn_load", use_container_width=True)

        # Xử lý Shuffle
        if shuffle_btn:
            steps = st.session_state.difficulty
            engine.reset_and_shuffle(steps=steps)
            st.session_state.timer_running = False
            st.session_state.start_timestamp = None
            st.session_state.accumulated_time = 0.0
            st.session_state.ai_solution = None
            st.session_state.ai_step_idx = 0
            st.session_state.won_notified = False
            st.session_state.status_message = f"Đã xáo mới bàn cờ với {steps} bước đảo ngược (100% giải được)!"
            st.toast("Bàn cờ mới đã sẵn sàng!", icon="🔄")
            st.rerun()

        # Xử lý Auto Solve
        if solve_btn:
            if hasattr(engine.board_state, "to_tuple"):
                board_tuple = engine.board_state.to_tuple()
            else:
                board_tuple = tuple(val for row in engine.board_state.grid for val in row)

            if engine.is_win():
                st.toast("Bàn cờ hiện tại đã ở trạng thái giải rồi!", icon="🎯")
            else:
                algo_name = st.session_state.get("ai_algorithm", "IDA*")
                with st.spinner(f"AI đang tìm đường đi ngắn nhất bằng thuật toán {algo_name}..."):
                    start_t = time.perf_counter()
                    if algo_name == "A*" and AStarSolver is not None:
                        solver = AStarSolver()
                        moves = solver.solve(board_tuple)
                    else:
                        solver = IDASolver(weight=2)
                        moves = solver.solve(board_tuple)
                    elapsed_solve = time.perf_counter() - start_t

                    if moves:
                        st.session_state.ai_solution = moves
                        st.session_state.ai_step_idx = 0
                        calc_time = getattr(solver, "execution_time", elapsed_solve)
                        calc_nodes = getattr(solver, "nodes_expanded", len(moves))
                        st.session_state.ai_stats = {
                            "time": calc_time,
                            "nodes": calc_nodes,
                            "length": len(moves),
                            "algo": algo_name,
                        }
                        st.session_state.status_message = f"AI ({algo_name}) đã tìm thấy lời giải {len(moves)} bước trong {calc_time:.3f}s!"
                        st.toast(f"Đã tìm thấy lời giải {len(moves)} bước ({algo_name})!", icon="⚡")
                        st.rerun()
                    else:
                        st.error("Không tìm thấy lời giải trong thời gian giới hạn hoặc bàn cờ vô nghiệm.")

        # Xử lý Save
        if save_btn:
            engine.board_state.elapsed_time = elapsed
            if save_game(engine.board_state):
                st.toast("Đã lưu trạng thái ván đấu vào data/save.dat!", icon="💾")
                st.session_state.status_message = "Đã lưu ván đấu thành công."
            else:
                st.error("Lỗi khi lưu game.")

        # Xử lý Load
        if load_btn:
            loaded_state = load_game()
            if loaded_state:
                engine.board_state = loaded_state
                st.session_state.timer_running = False
                st.session_state.start_timestamp = None
                st.session_state.accumulated_time = loaded_state.elapsed_time
                st.session_state.ai_solution = None
                st.session_state.ai_step_idx = 0
                st.session_state.won_notified = False
                st.toast("Đã tải lại ván đấu từ data/save.dat!", icon="📂")
                st.session_state.status_message = "Đã tải ván đấu thành công."
                st.rerun()
            else:
                st.warning("Chưa có file lưu hoặc dữ liệu file không hợp lệ.")

        # Phân cấp độ khó
        st.caption("**Độ khó (Difficulty / Số bước xáo)**")
        diff_cols = st.columns(3, gap="small")
        with diff_cols[0]:
            if st.button("🟢 Dễ (10)", key="diff_10", use_container_width=True):
                st.session_state.difficulty = 10
                engine.reset_and_shuffle(steps=10)
                st.session_state.timer_running = False
                st.session_state.accumulated_time = 0.0
                st.session_state.ai_solution = None
                st.session_state.won_notified = False
                st.session_state.status_message = "Chế độ Dễ (10 bước xáo)!"
                st.rerun()
        with diff_cols[1]:
            if st.button("🟠 Vừa (30)", key="diff_30", use_container_width=True):
                st.session_state.difficulty = 30
                engine.reset_and_shuffle(steps=30)
                st.session_state.timer_running = False
                st.session_state.accumulated_time = 0.0
                st.session_state.ai_solution = None
                st.session_state.won_notified = False
                st.session_state.status_message = "Chế độ Trung bình (30 bước xáo)!"
                st.rerun()
        with diff_cols[2]:
            if st.button("🔴 Khó (50)", key="diff_50", use_container_width=True):
                st.session_state.difficulty = 50
                engine.reset_and_shuffle(steps=50)
                st.session_state.timer_running = False
                st.session_state.accumulated_time = 0.0
                st.session_state.ai_solution = None
                st.session_state.won_notified = False
                st.session_state.status_message = "Chế độ Khó (50 bước xáo)!"
                st.rerun()

        # Bảng xếp hạng Top 10
        st.subheader("🏆 Bảng Xếp Hạng Top 10", divider="rainbow")
        leaderboard_data = load_leaderboard()

        if leaderboard_data:
            medals = ["🥇 1", "🥈 2", "🥉 3", "4", "5", "6", "7", "8", "9", "10"]
            rows_html = ""
            for i, rec in enumerate(leaderboard_data):
                rank_badge = medals[i] if i < len(medals) else str(i + 1)
                rank_class = f"rank-{i+1}" if i < 3 else "rank-normal"
                rows_html += f"""
                <tr class="{rank_class}">
                    <td style="font-weight: 800; font-size: 1.05rem;">{rank_badge}</td>
                    <td><strong>{rec.player_name}</strong></td>
                    <td><span class="badge-steps">{rec.step_count}</span></td>
                    <td style="font-weight: 700;">{rec.elapsed_time:.1f}s</td>
                    <td style="color: inherit; opacity: 0.85; font-size: 0.85rem;">{rec.date_played}</td>
                </tr>
                """

            table_html = f"""
            <div class="leaderboard-card">
                <table class="leaderboard-table">
                    <thead>
                        <tr>
                            <th style="width: 14%;">Hạng</th>
                            <th style="width: 32%;">Người chơi</th>
                            <th style="width: 18%;">Số bước</th>
                            <th style="width: 16%;">Thời gian</th>
                            <th style="width: 20%;">Ngày chơi</th>
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
            st.caption("Chưa có thành tích nào được ghi nhận.")

        # Nhập ma trận từ bên ngoài
        with st.expander("📥 Nhập Bàn Cờ Tùy Biến (Kiểm tra tính giải được)"):
            st.caption("Nhập dãy 16 số (0-15 phân cách bằng khoảng trắng hoặc dấu phẩy):")
            sample_val = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 0 15"
            raw_input = st.text_area("Ma trận:", value=sample_val, height=70)
            if st.button("Kiểm tra & Nạp bàn cờ", key="btn_custom_input", use_container_width=True):
                is_valid, msg, custom_grid = parse_and_validate_input(raw_input)
                if is_valid and custom_grid:
                    flat = [x for row in custom_grid for x in row]
                    empty_idx = flat.index(0)
                    engine.board_state = BoardState(
                        size=4,
                        grid=custom_grid,
                        empty_pos=(empty_idx // 4, empty_idx % 4),
                        step_count=0,
                        elapsed_time=0.0,
                    )
                    st.session_state.timer_running = False
                    st.session_state.accumulated_time = 0.0
                    st.session_state.ai_solution = None
                    st.session_state.won_notified = False
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
