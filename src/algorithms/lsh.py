"""
Thuật toán 3: Random Hyperplane LSH (Locality Sensitive Hashing - Băm nhạy ngữ cảnh).

Tác dụng trong dự án:
    - Kế thừa `BaseVectorIndex`.
    - Sinh m siêu phẳng ngẫu nhiên qua gốc tọa độ. Với mỗi vector, tính tích vô hướng với từng siêu phẳng để tạo mã băm m-bit (0 hoặc 1).
    - Gom các vector có góc tương tự vào cùng ngăn băm (hash bucket).
    - Khi tìm kiếm: Chỉ tính khoảng cách với các ứng viên nằm trong cùng bucket (hoặc bucket lân cận lệch 1 bit), giúp giảm đáng kể số lượng phép tính so với Linear Scan.
    - Thuật toán tìm kiếm xấp xỉ (ANN), phù hợp nhất với độ đo Cosine.
"""
