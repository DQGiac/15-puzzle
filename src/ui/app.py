"""
Module điều phối giao diện chính của ứng dụng Streamlit.

Tác dụng trong dự án:
    - Thiết lập cấu hình trang (tiêu đề, icon, layout 'wide').
    - Khởi tạo và lưu trữ phiên làm việc (st.session_state) như VectorEngineManager.
    - Điều hướng giữa 2 Tab chức năng:
        + Tab 1: Quản lý dữ liệu vector (tab_management).
        + Tab 2: Tìm kiếm tương đồng và Benchmark 5 thuật toán (tab_benchmark).
"""
