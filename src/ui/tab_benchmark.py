"""
Giao diện Tab 2: Tìm kiếm tương đồng và Benchmark so sánh 5 thuật toán (vai trò FAISS thu nhỏ).

Tác dụng trong dự án:
    - Cho phép người dùng chọn từ vựng truy vấn (query word), độ đo (Cosine hoặc Euclidean), và số lượng kết quả K (Top-K).
    - Thực thi tìm kiếm bằng cả 5 thuật toán: Linear Scan (Ground Truth), KD-Tree, LSH, IVF-Flat, HNSW.
    - Hiển thị bảng so sánh trực quan:
        + Kết quả Top-K từ gần nhất của từng thuật toán.
        + Thời gian thực thi (ms/us) bằng `time.perf_counter()`.
        + Độ chính xác Recall@K so với kết quả chuẩn của Linear Scan.
"""
