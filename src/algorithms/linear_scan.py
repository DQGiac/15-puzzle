"""
Thuật toán 1: Linear Scan (Quét tuyến tính vét cạn).

Tác dụng trong dự án:
    - Kế thừa `BaseVectorIndex`.
    - Duyệt qua toàn bộ N vector trong cơ sở dữ liệu để tính khoảng cách với vector truy vấn ($O(N \\cdot d)$).
    - Sử dụng `BoundedMaxHeap` để duy trì Top-K vector gần nhất.
    - Đạt độ chính xác tuyệt đối 100%, được dùng làm **Ground Truth** (đáp án chuẩn) để đo Recall@K cho các thuật toán xấp xỉ còn lại.
"""
