"""
Cài đặt cấu trúc dữ liệu HashTable (Bảng băm phân giải xung đột bằng Chaining).

Tác dụng trong dự án 15-Puzzle:
    - Lưu trữ các trạng thái bàn cờ (tuple 16 số) và chi phí g nhỏ nhất tương ứng.
    - Phục vụ thuật toán AI (IDA*, A*) để phát hiện và cắt tỉa các nhánh lặp lại.
    - Dung lượng mặc định: 100,003 buckets (số nguyên tố) theo tài liệu thiết kế.
"""

class HashTable:
    """Bảng băm phân giải xung đột bằng danh sách liên kết đơn (Chaining)."""

    def __init__(self, cap: int = 100003):
        self.cap = cap
        self.size = 0
        self.buckets = [[] for _ in range(cap)]

    def _hash(self, key) -> int:
        return hash(key) % self.cap

    def put(self, key, value) -> None:
        """Thêm hoặc cập nhật cặp (key, value)."""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, kv in enumerate(bucket):
            if kv[0] == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

    def get(self, key, default=None):
        """Lấy giá trị ứng với key, nếu không tồn tại trả về default."""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for kv in bucket:
            if kv[0] == key:
                return kv[1]
        return default

    def contains(self, key) -> bool:
        """Kiểm tra key có tồn tại trong bảng băm không."""
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for kv in bucket:
            if kv[0] == key:
                return True
        return False

    def __contains__(self, key) -> bool:
        return self.contains(key)

    def __getitem__(self, key):
        val = self.get(key)
        if val is None and not self.contains(key):
            raise KeyError(key)
        return val

    def __setitem__(self, key, value):
        self.put(key, value)

    def remove(self, key) -> bool:
        """Xóa key khỏi bảng băm."""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, kv in enumerate(bucket):
            if kv[0] == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def clear(self) -> None:
        """Xóa toàn bộ các phần tử trong bảng băm."""
        self.buckets = [[] for _ in range(self.cap)]
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __del__(self):
        self.clear()
        self.buckets = None
        self.size = 0

    def __str__(self) -> str:
        elements = []
        if self.buckets:
            for bucket in self.buckets:
                for kv in bucket:
                    elements.append(f"{repr(kv[0])}: {repr(kv[1])}")
        return "{" + ", ".join(elements) + "}"