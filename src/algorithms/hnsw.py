"""
Thuật toán 5: HNSW (Hierarchical Navigable Small World - Đồ thị thế giới nhỏ phân tầng).

Tác dụng trong dự án:
    - Kế thừa `BaseVectorIndex`.
    - Xây dựng đồ thị tìm kiếm đa tầng lấy cảm hứng từ cấu trúc Skip List:
        + Tầng trên cùng có ít đỉnh, cạnh nối xa giúp nhảy nhanh qua các vùng không gian vector.
        + Tầng 0 chứa toàn bộ N đỉnh với các liên kết chi tiết hơn.
    - Tìm kiếm: Bắt đầu từ đỉnh vào (entry point) ở tầng cao nhất, nhảy tham lam (greedy) sang đỉnh gần hơn, hạ dần xuống tầng 0 rồi tìm kiếm láng giềng cục bộ để lấy Top-K.
    - Đạt thời gian tìm kiếm xấp xỉ $O(\\log N \\cdot d)$, là thuật toán ANN hiện đại được dùng phổ biến trong FAISS và Milvus.
"""
