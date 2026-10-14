"""
Định nghĩa lớp trừu tượng BaseVectorIndex làm chuẩn chung cho 5 thuật toán tìm kiếm vector.

Tác dụng trong dự án:
    - Đảm bảo tính đa hình (Polymorphism) trong kiến trúc OOP.
    - Khai báo các phương thức trừu tượng bắt buộc:
        + `build(records)`: Xây dựng cấu trúc chỉ mục từ danh sách VectorRecord.
        + `search(query_vector, k, metric)`: Tìm kiếm Top-K vector gần nhất theo độ đo khoảng cách/tương đồng.
"""
