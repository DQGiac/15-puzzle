"""
Cài đặt Bảng Băm (HashTable) giải quyết xung đột bằng Separate Chaining.
Dùng để lưu vết các trạng thái bàn cờ đã duyệt qua trong thuật toán tìm kiếm.
"""


class HashTable:
    """Bảng băm sử dụng mảng bucket và danh sách liên kết/mảng lồng."""

    def __init__(self, cap: int = 1000):
        self.cap = cap
        self.size = 0
        self.buckets = [[] for _ in range(cap)]

    def _hash(self, key) -> int:
        return hash(key) % self.cap

    def put(self, key, value):
        """Thêm hoặc cập nhật giá trị cho khóa key."""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, kv in enumerate(bucket):
            if kv[0] == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

    def get(self, key, default=None):
        """Lấy giá trị của key, trả về default nếu không tồn tại."""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for kv in bucket:
            if kv[0] == key:
                return kv[1]
        return default

    def contains(self, key) -> bool:
        """Kiểm tra key có tồn tại trong bảng băm hay không."""
        idx = self._hash(key)
        for kv in self.buckets[idx]:
            if kv[0] == key:
                return True
        return False

    def remove(self, key) -> bool:
        """Xóa key khỏi bảng băm. Trả về True nếu xóa thành công, False nếu không tìm thấy."""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, kv in enumerate(bucket):
            if kv[0] == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def clear(self):
        """Xóa toàn bộ các phần tử trong bảng băm."""
        self.buckets = [[] for _ in range(self.cap)]
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __contains__(self, key) -> bool:
        return self.contains(key)

    def __getitem__(self, key):
        idx = self._hash(key)
        for kv in self.buckets[idx]:
            if kv[0] == key:
                return kv[1]
        raise KeyError(f"Không tìm thấy key: {key}")

    def __setitem__(self, key, value):
        self.put(key, value)

    def __str__(self) -> str:
        elements = []
        for bucket in self.buckets:
            for kv in bucket:
                elements.append(f"{repr(kv[0])}: {repr(kv[1])}")
        return "{" + ", ".join(elements) + "}"
