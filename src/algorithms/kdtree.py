"""
Thuật toán 2: KD-Tree (Cây k-chiều phân chia không gian).

Tác dụng trong dự án:
    - Kế thừa `BaseVectorIndex`.
    - Dựng cây KD-Tree: Tại mỗi tầng, chia không gian theo giá trị trung vị (median) của trục tọa độ xoay vòng (axis = depth % dimension).
    - Tìm kiếm Top-K láng giềng gần nhất với cơ chế cắt tỉa nhánh (branch pruning) khi khoảng cách siêu phẳng vượt quá bán kính hiện tại trong BoundedMaxHeap.
    - Thời gian tìm kiếm trung bình $O(\\log N \\cdot d)$.
"""
