"""
Cài đặt cấu trúc dữ liệu LinkedQueue (Hàng đợi danh sách liên kết - FIFO).

Tác dụng trong dự án:
    - Phục vụ các giải thuật duyệt theo tầng, duyệt chiều rộng (BFS) trong cây (KD-Tree) và đồ thị phân tầng (HNSW).
    - Các thao tác chính: `enqueue(item)`, `dequeue()`, `peek()`, `is_empty()`, `size()`.
    - Ràng buộc: Tự cài đặt bằng con trỏ nút liên kết hai đầu (head/tail), tuyệt đối không dùng `collections.deque`.
"""
