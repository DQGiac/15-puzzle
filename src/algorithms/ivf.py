"""
Thuật toán 4: IVF-Flat (Inverted File Index - Chỉ mục đảo phân cụm).

Tác dụng trong dự án:
    - Kế thừa `BaseVectorIndex`.
    - Giai đoạn dựng chỉ mục: Sử dụng thuật toán K-Means tự cài đặt để gom N vector thành C cụm, xác định C tâm cụm (centroid), và lưu vector của từng cụm vào danh sách đảo (`inverted_lists`).
    - Giai đoạn tìm kiếm: So sánh truy vấn với C tâm cụm, chỉ chọn `nprobe` cụm gần nhất và duyệt các vector trong những cụm đó để lấy Top-K.
    - Cân bằng giữa tốc độ tìm kiếm và Recall (tăng `nprobe` sẽ tăng độ chính xác nhưng giảm tốc độ).
"""
