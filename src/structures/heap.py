"""
Cài đặt cấu trúc dữ liệu MinHeap (Binary Min-Heap).

Tác dụng trong dự án 15-Puzzle:
    - Quản lý hàng đợi ưu tiên (Priority Queue) cho thuật toán A* Search.
    - Duyệt nút có hàm đánh giá f = g + h nhỏ nhất trước.
    - Cài đặt thuần túy với sift-up, sift-down trên mảng mà không dùng `heapq`.
"""

class MinHeap:
    """Min-Heap nhị phân tự cài đặt."""

    def __init__(self):
        self.heap = []

    def push(self, item):
        """Thêm phần tử vào heap và điều chỉnh heap (sift-up)."""
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        """Lấy ra phần tử nhỏ nhất ở đỉnh heap và điều chỉnh heap (sift-down)."""
        if self.is_empty():
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)

        return min_item

    def peek(self):
        """Xem phần tử nhỏ nhất ở đỉnh heap mà không lấy ra."""
        return self.heap[0] if not self.is_empty() else None

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def __len__(self) -> int:
        return len(self.heap)

    def _sift_up(self, id: int):
        parent_id = (id - 1) // 2
        while id > 0 and self.heap[id] < self.heap[parent_id]:
            self.heap[id], self.heap[parent_id] = self.heap[parent_id], self.heap[id]
            id = parent_id
            parent_id = (id - 1) // 2

    def _sift_down(self, id: int):
        n = len(self.heap)
        while True:
            left = 2 * id + 1
            right = 2 * id + 2
            smallest = id

            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest != id:
                self.heap[id], self.heap[smallest] = self.heap[smallest], self.heap[id]
                id = smallest
            else:
                break
