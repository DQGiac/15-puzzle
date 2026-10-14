"""
Cài đặt cấu trúc dữ liệu BoundedMaxHeap (Max-Heap nhị phân giới hạn dung lượng K).

Tác dụng trong dự án:
    - Lưu giữ Top-K láng giềng gần nhất (khoảng cách nhỏ nhất) trong quá trình tìm kiếm của các thuật toán.
    - Cơ chế: Giữ tối đa K phần tử; phần tử có khoảng cách lớn nhất nằm ở đỉnh heap. Khi gặp phần tử mới gần hơn đỉnh, thay thế đỉnh và thực hiện sift-down O(log K).
    - Giúp tìm Top-K với độ phức tạp thời gian O(N log K) thay vì phải sắp xếp toàn bộ tập O(N log N).
    - Ràng buộc: Tự cài đặt thao tác heapify, sift-up, sift-down trên mảng, tuyệt đối không dùng thư viện `heapq`.
"""
