"""
Giao diện Bàn cờ và Trò chơi 15-Puzzle mô phỏng chính xác bản gốc C++ Raylib.
Bao gồm:
    - Bàn cờ Catppuccin Mocha (#1E1E2E) với các ô vuông hoàn hảo 1:1, xích sát nhau (gap 5px).
    - Gradient màu ô số chuẩn C++:
        r = 30 + val * 14
        g = 60 + val * 8
        b = 180 - val * 6
    - Đồng hồ định dạng mm:ss như trong GameScene.cpp.
    - Phím tắt bàn phím: 1/2/3 (Dễ/Vừa/Khó), R (Xáo), U (Undo), Space (AI giải), Mũi tên (Di chuyển ô).
    - Bộ nạp level mẫu gốc: Easy (3 bước), Medium (4 bước), Hard (13 bước).
    - AI Playback Controller mượt mà, không bị giật lag hay treo luồng.
"""

import time
from html import escape
import streamlit as st
import streamlit.components.v1 as components

from src.models.board_state import BoardState
from src.models.record import ScoreRecord
from src.logic.engine import GameEngine
from src.logic.validator import parse_and_validate_input
from src.algorithms.ida_solver import IDASolver
try:
    from src.algorithms.a_star_solver import AStarSolver
except ImportError:
    AStarSolver = None

from src.storage.storage import add_score_record

# 3 Bàn cờ mẫu chuẩn từ C++ levels/
LEVEL_EASY = [
    [1, 2, 3, 4],
    [5, 6, 0, 7],
    [9, 10, 11, 8],
    [13, 14, 15, 12],
]

LEVEL_MEDIUM = [
    [1, 2, 3, 4],
    [5, 0, 6, 8],
    [9, 10, 7, 11],
    [13, 14, 15, 12],
]

LEVEL_HARD = [
    [5, 1, 2, 4],
    [9, 6, 3, 8],
    [13, 10, 7, 0],
    [14, 11, 15, 12],
]


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
        # Nạp mặc định level Easy
        engine.board_state.grid = [row[:] for row in LEVEL_EASY]
        engine.board_state.empty_pos = (1, 2)
        st.session_state.game_engine = engine

    if "ai_algorithm" not in st.session_state:
        st.session_state.ai_algorithm = "IDA*"

    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False

    if "start_timestamp" not in st.session_state:
        st.session_state.start_timestamp = None

    if "accumulated_time" not in st.session_state:
        st.session_state.accumulated_time = 0.0

    if "ai_solution" not in st.session_state:
        st.session_state.ai_solution = None

    if "ai_step_idx" not in st.session_state:
        st.session_state.ai_step_idx = 0

    if "ai_stats" not in st.session_state:
        st.session_state.ai_stats = None

    if "ai_auto_playing" not in st.session_state:
        st.session_state.ai_auto_playing = False

    if "playback_speed" not in st.session_state:
        st.session_state.playback_speed = 0.2

    if "won_notified" not in st.session_state:
        st.session_state.won_notified = False

    if "status_message" not in st.session_state:
        st.session_state.status_message = "Sẵn sàng! Dùng chuột click ô số hoặc bấm phím mũi tên để trượt."


def get_current_time() -> float:
    """Tính thời gian ván chơi hiện tại theo giây."""
    if st.session_state.get("timer_running", False) and st.session_state.get("start_timestamp"):
        return st.session_state.accumulated_time + (time.time() - st.session_state.start_timestamp)
    return st.session_state.get("accumulated_time", 0.0)


def stop_timer() -> float:
    """Dừng bộ đếm thời gian và trả về thời gian tổng cộng."""
    elapsed = get_current_time()
    st.session_state.timer_running = False
    st.session_state.accumulated_time = elapsed
    st.session_state.start_timestamp = None
    return elapsed


def format_time_mmss(seconds_float: float) -> str:
    """Định dạng thời gian mm:ss.t, với độ chính xác một phần mười giây."""
    # Dùng phép cắt thay vì làm tròn để đồng hồ không hiển thị trước thời gian thực.
    total_tenths = int(seconds_float * 10)
    total_sec, tenths = divmod(total_tenths, 10)
    minutes = total_sec // 60
    seconds = total_sec % 60
    return f"{minutes:d}:{seconds:02d}.{tenths}"


def render_live_timer():
    """Vẽ đồng hồ; JavaScript sẽ cập nhật phần hiển thị mỗi 0,1 giây."""
    engine: GameEngine = st.session_state.game_engine
    elapsed = get_current_time()
    engine.board_state.elapsed_time = elapsed
    is_running = str(st.session_state.get("timer_running", False)).lower()
    start_timestamp = st.session_state.get("start_timestamp") or 0.0
    accumulated_time = st.session_state.get("accumulated_time", 0.0)
    st.markdown(
        '<div class="raylib-header-box">'
        '<div class="raylib-title">15 PUZZLE</div>'
        f'<div class="raylib-timer" data-timer-running="{is_running}" '
        f'data-start-timestamp="{start_timestamp}" '
        f'data-accumulated-time="{accumulated_time}">{format_time_mmss(elapsed)}</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def inject_cpp_board_styler_and_shortcuts():
    """
    Tiêm mã JS tự động ép 16 ô cờ VUÔNG HOÀN HẢO 1:1, XÍCH SÁT NHAU (gap 5px),
    áp dụng màu gradient C++ và bắt toàn bộ phím tắt bàn phím (Mũi tên, R, U, 1, 2, 3, Space).
    """
    js_code = """
    <script>
    (function() {
        const doc = window.parent.document;
        if (!doc) return;

        function getTileButtons() {
            const allButtons = Array.from(doc.querySelectorAll('button'));
            return allButtons.filter(btn => {
                const text = btn.innerText ? btn.innerText.trim() : '';
                const val = parseInt(text);
                const isNum = !isNaN(val) && val >= 1 && val <= 15 && text === String(val);
                const isEmpty = (text === '' || text === ' ') && btn.disabled;
                return isNum || isEmpty;
            });
        }

        function getCommonAncestor(el1, el2) {
            if (!el1 || !el2) return null;
            const ancestors = new Set();
            let curr = el1;
            while (curr) {
                ancestors.add(curr);
                curr = curr.parentElement;
            }
            curr = el2;
            while (curr) {
                if (ancestors.has(curr)) return curr;
                curr = curr.parentElement;
            }
            return null;
        }

        function applyCppStyles() {
            const tileBtns = getTileButtons();
            if (tileBtns.length !== 16) return;

            // Tìm container chung bao bọc toàn bộ 16 ô cờ và header
            const anchor = doc.getElementById('c-raylib-board-frame');
            const boardContainer = (anchor ? getCommonAncestor(anchor, tileBtns[15]) : null) || getCommonAncestor(tileBtns[0], tileBtns[15]);

            if (boardContainer && !boardContainer.__raylib_styled) {
                boardContainer.__raylib_styled = true;
                boardContainer.style.setProperty('max-width', '420px', 'important');
                boardContainer.style.setProperty('margin', '0 auto 12px auto', 'important');
                boardContainer.style.setProperty('background', '#1E1E2E', 'important');
                boardContainer.style.setProperty('border', '2px solid #313244', 'important');
                boardContainer.style.setProperty('border-radius', '18px', 'important');
                boardContainer.style.setProperty('padding', '14px', 'important');
                boardContainer.style.setProperty('box-shadow', '0 12px 30px rgba(0,0,0,0.55)', 'important');
                boardContainer.style.setProperty('box-sizing', 'border-box', 'important');
            }

            // Đo độ rộng thực tế của một ô trên màn hình (để ép chiều cao = chiều rộng)
            const firstCol = tileBtns[0].closest('[data-testid="stColumn"]');
            const tileWidth = (firstCol && firstCol.getBoundingClientRect().width > 20)
                ? Math.round(firstCol.getBoundingClientRect().width)
                : (tileBtns[0].getBoundingClientRect().width > 20 ? Math.round(tileBtns[0].getBoundingClientRect().width) : 88);

            const processedRows = new Set();

            tileBtns.forEach(btn => {
                btn.classList.add('c-square-tile');

                // Ép cột không padding và không min-width
                const col = btn.closest('[data-testid="stColumn"]');
                if (col) {
                    col.style.setProperty('padding', '0px', 'important');
                    col.style.setProperty('margin', '0px', 'important');
                    col.style.setProperty('min-width', '0px', 'important');

                    const row = col.parentElement;
                    if (row && !processedRows.has(row)) {
                        processedRows.add(row);
                        row.style.setProperty('gap', '5px', 'important');
                        row.style.setProperty('margin-bottom', '5px', 'important');
                        row.style.setProperty('margin-top', '0px', 'important');
                        row.style.setProperty('display', 'flex', 'important');
                    }
                }

                // ÉP Ô CỜ VUÔNG HOÀN HẢO 1:1 (Chiều cao = Chiều rộng)
                btn.style.setProperty('aspect-ratio', '1 / 1', 'important');
                btn.style.setProperty('width', '100%', 'important');
                btn.style.setProperty('padding', '0px', 'important');
                btn.style.setProperty('margin', '0px', 'important');
                btn.style.setProperty('display', 'flex', 'important');
                btn.style.setProperty('align-items', 'center', 'important');
                btn.style.setProperty('justify-content', 'center', 'important');
                btn.style.setProperty('border-radius', '12px', 'important');

                if (tileWidth > 20) {
                    btn.style.setProperty('height', tileWidth + 'px', 'important');
                    btn.style.setProperty('min-height', tileWidth + 'px', 'important');
                    btn.style.setProperty('max-height', tileWidth + 'px', 'important');
                }

                // Áp dụng gradient màu C++
                const text = btn.innerText ? btn.innerText.trim() : '';
                const val = parseInt(text);

                if (!isNaN(val) && val >= 1 && val <= 15) {
                    const r = 30 + val * 14;
                    const g = 60 + val * 8;
                    const b = 180 - val * 6;
                    btn.style.setProperty('background', `rgb(${r}, ${g}, ${b})`, 'important');
                    btn.style.setProperty('background-color', `rgb(${r}, ${g}, ${b})`, 'important');
                    btn.style.setProperty('color', '#FFFFFF', 'important');
                    btn.style.setProperty('border', 'none', 'important');
                    btn.style.setProperty('opacity', '1.0', 'important');
                    btn.style.setProperty('font-size', '1.95rem', 'important');
                    btn.style.setProperty('font-weight', '900', 'important');
                    btn.style.setProperty('box-shadow', '0 4px 8px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.3)', 'important');
                } else {
                    btn.style.setProperty('background', '#181825', 'important');
                    btn.style.setProperty('background-color', '#181825', 'important');
                    btn.style.setProperty('border', '2px dashed #313244', 'important');
                    btn.style.setProperty('opacity', '0.35', 'important');
                    btn.style.setProperty('box-shadow', 'inset 0 3px 8px rgba(0,0,0,0.6)', 'important');
                }
            });
        }

        applyCppStyles();
        requestAnimationFrame(applyCppStyles);
        setTimeout(applyCppStyles, 50);
        setTimeout(applyCppStyles, 150);
        setTimeout(applyCppStyles, 400);

        window.addEventListener('resize', applyCppStyles);

        // Chỉ cập nhật chữ số của đồng hồ ở trình duyệt. Nhờ đó click tile
        // không bị xung đột với một Streamlit fragment đang tự rerun.
        if (window.__puzzle_timer_interval) {
            window.clearInterval(window.__puzzle_timer_interval);
        }
        function updatePuzzleTimer() {
            const timer = doc.querySelector('.raylib-timer');
            if (!timer || timer.dataset.timerRunning !== 'true') return;

            const accumulated = Number(timer.dataset.accumulatedTime) || 0;
            const startedAt = Number(timer.dataset.startTimestamp) || 0;
            const elapsed = accumulated + Math.max(0, Date.now() / 1000 - startedAt);
            const totalTenths = Math.floor(elapsed * 10);
            const totalSeconds = Math.floor(totalTenths / 10);
            const minutes = Math.floor(totalSeconds / 60);
            const seconds = String(totalSeconds % 60).padStart(2, '0');
            timer.textContent = `${minutes}:${seconds}.${totalTenths % 10}`;
        }
        updatePuzzleTimer();
        window.__puzzle_timer_interval = window.setInterval(updatePuzzleTimer, 100);

        if (!window.__cpp_board_observer) {
            window.__cpp_board_observer = true;
            const observer = new MutationObserver(() => {
                applyCppStyles();
            });
            observer.observe(doc.body, { childList: true, subtree: true });
        }

        if (window.__cpp_keys_active) return;
        window.__cpp_keys_active = true;

        doc.addEventListener('keydown', function(e) {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            // Xử lý các phím mũi tên di chuyển ô cờ kề ô trống
            if (e.key === 'ArrowUp' || e.key === 'ArrowDown' || e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
                const tileBtns = getTileButtons();
                if (tileBtns.length === 16) {
                    let emptyIdx = -1;
                    for (let i = 0; i < 16; i++) {
                        const t = tileBtns[i].innerText ? tileBtns[i].innerText.trim() : '';
                        const v = parseInt(t);
                        if (t === '' || t === ' ' || v === 0 || isNaN(v)) {
                            emptyIdx = i;
                            break;
                        }
                    }
                    if (emptyIdx !== -1) {
                        let targetIdx = -1;
                        if (e.key === 'ArrowUp' && emptyIdx + 4 < 16) targetIdx = emptyIdx + 4;
                        else if (e.key === 'ArrowDown' && emptyIdx - 4 >= 0) targetIdx = emptyIdx - 4;
                        else if (e.key === 'ArrowLeft' && emptyIdx % 4 < 3) targetIdx = emptyIdx + 1;
                        else if (e.key === 'ArrowRight' && emptyIdx % 4 > 0) targetIdx = emptyIdx - 1;

                        if (targetIdx !== -1 && tileBtns[targetIdx]) {
                            e.preventDefault();
                            tileBtns[targetIdx].click();
                            return;
                        }
                    }
                }
            }

            const key = e.key.toLowerCase();
            const allBtns = Array.from(doc.querySelectorAll('button'));
            function clickBtnByKw(kw) {
                const b = allBtns.find(btn => btn.innerText && btn.innerText.includes(kw));
                if (b) { b.click(); return true; }
                return false;
            }

            if (key === 'r') clickBtnByKw('[R]');
            else if (key === 'u' || (e.ctrlKey && key === 'z')) clickBtnByKw('[U]');
            else if (key === '1') clickBtnByKw('[1]');
            else if (key === '2') clickBtnByKw('[2]');
            else if (key === '3') clickBtnByKw('[3]');
            else if (e.code === 'Space') {
                if (clickBtnByKw('Tìm Lời Giải') || clickBtnByKw('Tự động')) e.preventDefault();
            }
        });
    })();
    </script>
    """
    components.html(js_code, height=0, width=0)


def load_preset_level(engine: GameEngine, level_matrix: list[list[int]]):
    """Nạp ma trận level chuẩn từ C++ levels/."""
    engine.board_state.grid = [row[:] for row in level_matrix]
    for r in range(4):
        for c in range(4):
            if level_matrix[r][c] == 0:
                engine.board_state.empty_pos = (r, c)
                break
    engine.board_state.step_count = 0
    engine.board_state.elapsed_time = 0.0
    engine.history.clear()
    st.session_state.timer_running = False
    st.session_state.accumulated_time = 0.0
    st.session_state.ai_solution = None
    st.session_state.ai_step_idx = 0
    st.session_state.ai_auto_playing = False
    st.session_state.won_notified = False


def render_tab_puzzle():
    """Hiển thị giao diện chính của bàn cờ 15-Puzzle theo phong cách C++."""
    init_session_state()
    inject_cpp_board_styler_and_shortcuts()

    engine: GameEngine = st.session_state.game_engine
    is_game_won = engine.is_win()

    # Dừng đồng hồ khi chiến thắng
    if is_game_won and not st.session_state.won_notified:
        stop_timer()
        st.session_state.won_notified = True
        st.session_state.ai_auto_playing = False
        st.session_state.status_message = "CHÚC MỪNG! Bạn đã hoàn thành 15-Puzzle!"

    # Dùng cho màn hình chiến thắng và dữ liệu lưu điểm. Đồng hồ trên header
    # được JavaScript cập nhật độc lập, còn giá trị này luôn lấy từ Session State.
    elapsed = get_current_time()
    time_str = format_time_mmss(elapsed)

    # =========================================================================
    # BỐ CỤC 2 CỘT: CỘT TRÁI (BÀN CỜ C++) - CỘT PHẢI (AI SOLVER & CÔNG CỤ)
    # =========================================================================
    col_board, col_controls = st.columns([1.15, 1], gap="large")

    # -------------------------------------------------------------------------
    # CỘT TRÁI: BÀN CỜ GIAO DIỆN C++ RAYLIB (VUÔNG HOÀN HẢO & XÍCH SÁT NHAU)
    # -------------------------------------------------------------------------
    with col_board:
        with st.container():
            # Header bàn cờ và anchor nhận diện cho CSS/JS
            st.markdown('<div id="c-raylib-board-frame" style="display:none;"></div>', unsafe_allow_html=True)
            render_live_timer()

            grid = engine.board_state.grid
            size = engine.board_state.size
            valid_moves = set(engine.get_valid_moves())

            for r in range(size):
                cells = st.columns(size, gap="small")
                for c in range(size):
                    val = grid[r][c]
                    tile_can_move = (r, c) in valid_moves
                    btn_key = f"btn_slot_{r}_{c}"

                    with cells[c]:
                        if val == 0:
                            st.button(" ", key=btn_key, disabled=True, use_container_width=True)
                        else:
                            btn_clicked = st.button(
                                str(val),
                                key=btn_key,
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
                                    st.session_state.status_message = "CHÚC MỪNG! Bạn đã hoàn thành xuất sắc!"
                                else:
                                    st.session_state.status_message = f"Đã trượt ô {val} vào ô trống."
                                st.rerun()

            # Footer thông số bên dưới bàn cờ
            solving_html = ""
            if st.session_state.ai_auto_playing and st.session_state.ai_solution:
                solving_html = f'<div class="raylib-solving-status">AI đang giải... ({st.session_state.ai_step_idx}/{len(st.session_state.ai_solution)})</div>'

            footer_html = (
                f'<div class="raylib-footer-box">'
                f'<div class="raylib-step-count">Số bước: {engine.board_state.step_count}</div>'
                f'<div class="raylib-status-message" title="{escape(st.session_state.status_message, quote=True)}">'
                f'{escape(st.session_state.status_message)}</div>'
                f'</div>'
                f'{solving_html}'
            )
            st.markdown(footer_html, unsafe_allow_html=True)

        # Cụm nút nạp level C++ (1, 2, 3) và Xáo cờ, Undo
        st.caption("**Chọn bàn cờ (Phím 1/2/3 hoặc Xáo R):**")
        lvl_col1, lvl_col2, lvl_col3, lvl_col4, lvl_col5 = st.columns(5, gap="small")

        with lvl_col1:
            if st.button("🟢 [1] Dễ", use_container_width=True):
                load_preset_level(engine, LEVEL_EASY)
                st.session_state.status_message = "Đã nạp level Dễ từ levels/easy.txt (3 bước)!"
                st.rerun()

        with lvl_col2:
            if st.button("🟠 [2] Vừa", use_container_width=True):
                load_preset_level(engine, LEVEL_MEDIUM)
                st.session_state.status_message = "Đã nạp level Vừa từ levels/medium.txt (4 bước)!"
                st.rerun()

        with lvl_col3:
            if st.button("🔴 [3] Khó", use_container_width=True):
                load_preset_level(engine, LEVEL_HARD)
                st.session_state.status_message = "Đã nạp level Khó từ levels/hard.txt (13 bước)!"
                st.rerun()

        with lvl_col4:
            if st.button("🔄 [R] Xáo", use_container_width=True):
                engine.reset_and_shuffle(steps=30)
                st.session_state.timer_running = False
                st.session_state.accumulated_time = 0.0
                st.session_state.ai_solution = None
                st.session_state.ai_step_idx = 0
                st.session_state.ai_auto_playing = False
                st.session_state.won_notified = False
                st.session_state.status_message = "Đã xáo mới bàn cờ 30 bước đảo ngược!"
                st.rerun()

        with lvl_col5:
            undo_disabled = not engine.can_undo() or is_game_won
            if st.button("↩️ [U] Lùi", disabled=undo_disabled, use_container_width=True):
                if engine.undo():
                    st.session_state.status_message = "Đã lùi lại 1 bước."
                    st.rerun()

        # Màn hình chúc mừng nhập tên khi thắng
        if is_game_won:
            st.balloons()
            with st.container(border=True):
                st.markdown("### 🏆 CHÚC MỪNG! BẠN ĐÃ THẮNG!")
                st.caption(f"Thành tích: **{engine.board_state.step_count} bước** trong **{time_str}**")
                c_name, c_sub = st.columns([2, 1])
                with c_name:
                    p_name = st.text_input("Nhập tên lưu vào Top 10:", value="Player 1", max_chars=20)
                with c_sub:
                    st.write("")
                    st.write("")
                    if st.button("💾 Lưu Điểm", type="primary", use_container_width=True):
                        rec = ScoreRecord(
                            player_name=p_name.strip() or "Anonymous",
                            step_count=engine.board_state.step_count,
                            elapsed_time=elapsed,
                        )
                        add_score_record(rec)
                        st.toast("Đã ghi danh vào Bảng Vàng!", icon="🏆")
                        st.rerun()

    # -------------------------------------------------------------------------
    # CỘT PHẢI: AI SOLVER THÔNG MINH & TRÌNH DIỄN LỜI GIẢI
    # -------------------------------------------------------------------------
    with col_controls:
        st.subheader("🤖 AI Solver Thông Minh (IDA* & A*)", divider="rainbow")

        # Tùy chọn thuật toán AI
        algo_options = ["IDA* (Heuristic Manhattan)", "A* (MinHeap Queue)"]
        selected_algo = st.radio(
            "Thuật toán giải tự động:",
            options=algo_options,
            index=0 if "IDA*" in st.session_state.ai_algorithm else 1,
            horizontal=True,
        )
        st.session_state.ai_algorithm = "IDA*" if "IDA*" in selected_algo else "A*"

        # Nút kích hoạt AI giải
        if st.button("⚡ [Space] Tìm Lời Giải Ngay", type="primary", use_container_width=True):
            if is_game_won:
                st.toast("Bàn cờ hiện tại đã ở trạng thái đích rồi!", icon="🎯")
            else:
                board_tuple = engine.board_state.to_tuple()
                algo = st.session_state.ai_algorithm

                with st.spinner(f"AI đang tính toán lời giải ngắn nhất bằng {algo}..."):
                    start_t = time.perf_counter()
                    if algo == "A*" and AStarSolver is not None:
                        solver = AStarSolver(max_nodes=50000, max_time_seconds=12.0)
                        moves = solver.solve(board_tuple)
                    else:
                        solver = IDASolver(weight=2)
                        moves = solver.solve(board_tuple)
                    calc_time = time.perf_counter() - start_t

                    if moves:
                        st.session_state.ai_solution = moves
                        st.session_state.ai_step_idx = 0
                        st.session_state.ai_auto_playing = False
                        st.session_state.ai_stats = {
                            "algo": algo,
                            "time": getattr(solver, "execution_time", calc_time),
                            "nodes": getattr(solver, "nodes_expanded", len(moves)),
                            "steps": len(moves),
                        }
                        st.session_state.status_message = f"AI tìm ra lời giải {len(moves)} bước!"
                        st.toast(f"Đã tìm thấy lời giải {len(moves)} bước!", icon="⚡")
                        st.rerun()
                    else:
                        st.error("Không tìm thấy lời giải hoặc bàn cờ vượt quá giới hạn thời gian (12s).")

        # =====================================================================
        # BỘ ĐIỀU KHIỂN PHÁT LỜI GIẢI (PLAYBACK CONTROLLER)
        # =====================================================================
        if st.session_state.ai_solution:
            solution = st.session_state.ai_solution
            stats = st.session_state.ai_stats or {}
            curr_step = st.session_state.ai_step_idx

            st.write("")
            with st.container(border=True):
                st.markdown(
                    f"**Kết quả phân tích ({stats.get('algo', 'IDA*')}):** "
                    f"⏱️ **{stats.get('time', 0):.3f}s** | "
                    f"📏 **{len(solution)} bước** | "
                    f"🧠 **{stats.get('nodes', 0):,} nút duyệt**"
                )

                # Thanh tiến trình
                prog = curr_step / max(len(solution), 1)
                st.progress(prog, text=f"Tiến trình: Bước {curr_step}/{len(solution)}")

                # Tốc độ Auto-Play
                spd = st.slider(
                    "Tốc độ tự động giải (giây/bước):",
                    min_value=0.05,
                    max_value=1.0,
                    value=st.session_state.playback_speed,
                    step=0.05,
                )
                st.session_state.playback_speed = spd

                # Cụm nút Playback
                p1, p2, p3, p4 = st.columns(4, gap="small")
                with p1:
                    if st.session_state.ai_auto_playing:
                        if st.button("⏸️ Dừng", use_container_width=True):
                            st.session_state.ai_auto_playing = False
                            st.rerun()
                    else:
                        if st.button("▶️ Chạy", use_container_width=True, disabled=curr_step >= len(solution)):
                            st.session_state.ai_auto_playing = True
                            st.rerun()

                with p2:
                    if st.button("⏭️ 1 bước", use_container_width=True, disabled=curr_step >= len(solution)):
                        st.session_state.ai_auto_playing = False
                        apply_direction_move(engine, solution[curr_step])
                        st.session_state.ai_step_idx += 1
                        st.rerun()

                with p3:
                    if st.button("⏩ Xong", use_container_width=True, disabled=curr_step >= len(solution)):
                        st.session_state.ai_auto_playing = False
                        while st.session_state.ai_step_idx < len(solution):
                            apply_direction_move(engine, solution[st.session_state.ai_step_idx])
                            st.session_state.ai_step_idx += 1
                        st.session_state.status_message = "AI đã hoàn tất giải toàn bộ bàn cờ!"
                        st.rerun()

                with p4:
                    if st.button("❌ Hủy", use_container_width=True):
                        st.session_state.ai_solution = None
                        st.session_state.ai_step_idx = 0
                        st.session_state.ai_auto_playing = False
                        st.rerun()

                # Danh sách các bước tiếp theo
                upcoming = " ➔ ".join(solution[curr_step: curr_step + 8])
                if upcoming:
                    st.caption(f"**Các bước tiếp theo:** {upcoming}{' ...' if len(solution) > curr_step + 8 else ''}")

        # =====================================================================
        # NẠP MA TRẬN TÙY BIẾN
        # =====================================================================
        st.write("")
        with st.expander("📥 Nạp Ma Trận Tùy Biến (Kiểm tra tính giải được)"):
            st.caption("Nhập dãy 16 số phân tách bởi dấu cách hoặc phẩy (0 là ô trống):")
            sample_val = "1 2 3 4 5 6 0 7 9 10 11 8 13 14 15 12"
            raw_mat = st.text_area("Ma trận bàn cờ:", value=sample_val, height=70)

            if st.button("Kiểm tra & Nạp", key="btn_apply_matrix", use_container_width=True):
                is_valid, msg, grid_data = parse_and_validate_input(raw_mat)
                if is_valid and grid_data:
                    flat = [x for row in grid_data for x in row]
                    zero_pos = flat.index(0)
                    engine.board_state = BoardState(
                        size=4,
                        grid=grid_data,
                        empty_pos=(zero_pos // 4, zero_pos % 4),
                        step_count=0,
                        elapsed_time=0.0,
                    )
                    engine.history.clear()
                    st.session_state.timer_running = False
                    st.session_state.accumulated_time = 0.0
                    st.session_state.ai_solution = None
                    st.session_state.won_notified = False
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

    # =========================================================================
    # XỬ LÝ AUTO-PLAY AI PLAYBACK Ở CUỐI TRANG ĐỂ KHÔNG NUỐT NÚT PAUSE/CANCEL
    # =========================================================================
    if st.session_state.ai_auto_playing and st.session_state.ai_solution:
        sol = st.session_state.ai_solution
        idx = st.session_state.ai_step_idx
        if idx < len(sol) and not is_game_won:
            time.sleep(st.session_state.playback_speed)
            move_dir = sol[idx]
            apply_direction_move(engine, move_dir)
            st.session_state.ai_step_idx += 1
            if st.session_state.ai_step_idx >= len(sol) or engine.is_win():
                st.session_state.ai_auto_playing = False
                st.session_state.status_message = "🎉 AI đã hoàn tất toàn bộ bàn cờ!"
            st.rerun()
