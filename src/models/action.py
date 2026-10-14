"""
Định nghĩa lớp thực thể ActionRecord phục vụ cơ chế hoàn tác (Undo).

Tác dụng trong dự án:
    - Kế thừa từ `BaseEntity`.
    - Ghi lại vết của mỗi thao tác thay đổi dữ liệu:
        + Loại thao tác: `ADD` (thêm từ mới) hoặc `DELETE` (xóa từ).
        + Nhãn từ bị tác động (`label`).
        + `payload`: Dữ liệu vector cũ (nếu là thao tác DELETE) để có thể khôi phục nguyên vẹn.
    - Được đẩy vào `LinkedStack` (ngăn xếp Undo) mỗi khi có thay đổi trong `VectorEngineManager`.
"""
