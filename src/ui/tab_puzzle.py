"""
Giao diện Trò chơi 15-Puzzle (Lưới 4x4, Thống số và Bảng điều khiển).

Tác dụng trong dự án:
    - Hiển thị lưới bàn cờ 4x4 bằng các nút bấm Streamlit.
    - Hiển thị bảng số bước đi (Moves) và thời gian (Time).
    - Cung cấp các nút điều khiển: Shuffle, Auto Solve, Save, Load.
    - Cung cấp các nút chọn độ khó: Easy, Med, Hard.
    - Hiển thị bảng xếp hạng Top 10.
"""
import streamlit as st

def render_tab_puzzle():
    """Render giao diện thuần túy của 15-Puzzle."""
    board_col, controls_col = st.columns([1.1, 1], gap="large")

    # --- CỘT TRÁI: BÀN CỜ 4x4 SÁNG RỰC RỠ & THỐNG SỐ ---
    with board_col:
        # Lưới bàn cờ 4x4: Sử dụng type="primary" để ô số sáng bừng màu chủ đạo
        board_data = list(range(1, 16)) + [0]
        SIZE = 4
        for row in range(SIZE):
            cells = st.columns(SIZE, gap="small")
            for col in range(SIZE):
                index = row * SIZE + col
                val = board_data[index]
                with cells[col]:
                    if val == 0:
                        # Ô trống: nút rỗng bị disabled, nền tối tự nhiên để phân biệt với ô số
                        st.button(" ", key=f"tile_{index}", disabled=True, use_container_width=True)
                    else:
                        # Ô số: type="primary" làm ô số sáng màu primaryColor, chữ số in đậm to rõ
                        st.button(f"**{val}**", key=f"tile_{index}", type="primary", use_container_width=True)

        st.write("")  # Khoảng cách tự nhiên
        
        # Khung thống số: sử dụng màu sắc nhấn mạnh
        m_col1, m_col2 = st.columns(2)
        m_col1.metric(label=":rainbow[Moves]", value=0)
        m_col2.metric(label=":green[Time]", value="0.0s")

        # Thanh trạng thái
        st.info("Ready to play")

    # --- CỘT PHẢI: BẢNG ĐIỀU KHIỂN & BẢNG XẾP HẠNG ---
    with controls_col:
        # Thẻ điều khiển Controls với thanh gạch phân cách cầu vồng
        st.subheader("Controls", divider="rainbow")
        control_a, control_b = st.columns(2, gap="small")
        with control_a:
            st.button("🔄 :blue[**Shuffle (R)**]", key="btn_shuffle", use_container_width=True)
            st.button("💾 :violet[**Save (S)**]", key="btn_save", use_container_width=True)
        with control_b:
            st.button("⚡ :orange[**Auto Solve**]", key="btn_solve", use_container_width=True)
            st.button("📂 :green[**Load (L)**]", key="btn_load", use_container_width=True)

        # Phân cấp độ khó bằng 3 màu đặc trưng: Xanh lá (Dễ) - Cam (Vừa) - Đỏ (Khó)
        st.caption("**Difficulty (Scramble Steps)**")
        diff_cols = st.columns(3, gap="small")
        with diff_cols[0]:
            st.button("🟢 :green[**Easy (1)**]", key="diff_10", use_container_width=True)
        with diff_cols[1]:
            st.button("🟠 :orange[**Med (2)**]", key="diff_30", use_container_width=True)
        with diff_cols[2]:
            st.button("🔴 :red[**Hard (3)**]", key="diff_50", use_container_width=True)

        # Bảng xếp hạng Top 10 với thanh gạch phân cách cầu vồng
        st.subheader("🏆 Top 10", divider="rainbow")
        mock_scores = [
            {"Rank": "🥇 1", "Name": "Antigravity", "Moves": 38, "Time": "15.2s"},
            {"Rank": "🥈 2", "Name": "Player 1", "Moves": 45, "Time": "18.0s"},
            {"Rank": "🥉 3", "Name": "Player 2", "Moves": 58, "Time": "23.6s"},
        ]
        st.dataframe(
            mock_scores,
            use_container_width=True,
            hide_index=True,
        )
