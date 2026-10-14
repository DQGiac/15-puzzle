"""
Định nghĩa lớp thực thể VectorRecord đại diện cho một từ vựng và vector tương ứng.

Tác dụng trong dự án:
    - Kế thừa từ `BaseEntity`.
    - Lưu trữ nhãn từ vựng (`_label`), danh sách các giá trị thực của vector 50 chiều (`_values`).
    - Thuộc tính `_norm`: Độ dài Euclidean (chuẩn L2) được tính sẵn ngay khi khởi tạo để tăng tốc tính Cosine Similarity.
    - Phương thức `from_line(cls, line)`: Tách một dòng định dạng GloVe ('từ v1 v2 ... v50') thành đối tượng VectorRecord.
"""
