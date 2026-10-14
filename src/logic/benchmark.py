"""
Module BenchmarkRunner đo đạc hiệu năng và độ chính xác giữa các thuật toán.

Tác dụng trong dự án:
    - Đo thời gian dựng chỉ mục (Index Build Time) của từng thuật toán.
    - Đo thời gian tìm kiếm Top-K (Search Latency) bằng `time.perf_counter()`.
    - Tính độ chính xác Recall@K so với Ground Truth (Linear Scan):
        Recall@K = (Số từ chung giữa kết quả thuật toán và Linear Scan) / K
    - Tổng hợp kết quả thành dictionary hoặc cấu trúc bảng để giao diện Streamlit hiển thị trực quan.
"""
