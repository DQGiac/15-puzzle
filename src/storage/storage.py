"""
Module quản lý lưu trữ và đọc/ghi tệp dữ liệu vector.

Tác dụng trong dự án:
    - Đọc dữ liệu từ file `data/vectors.txt` (bộ Stanford GloVe 50 chiều), phân tích cú pháp mỗi dòng thành đối tượng `VectorRecord`.
    - Ghi dữ liệu vector từ bộ nhớ về file khi có thao tác thêm/xóa/hoàn tác nhằm đảm bảo tính bền vững (Persistence).
    - Xử lý các ngoại lệ liên quan đến file không tồn tại, sai định dạng dòng dữ liệu.
"""
