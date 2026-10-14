"""
Định nghĩa lớp thực thể cơ sở trừu tượng BaseEntity.

Tác dụng trong dự án:
    - Đảm bảo tính đóng gói (Encapsulation) và trừu tượng (Abstraction) theo chuẩn OOP.
    - Quản lý định danh duy nhất `_id` thông qua getter `@property id`.
    - Khai báo các phương thức trừu tượng:
        + `to_dict()`: Chuyển đổi thực thể thành dictionary (phục vụ tuần tự hóa).
        + `from_dict(cls, data)`: Khôi phục thực thể từ dictionary.
"""
