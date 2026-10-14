"""
Lớp VectorEngineManager điều phối toàn bộ hệ thống Vector Search Engine.

Tác dụng trong dự án:
    - Quản lý tập dữ liệu vector trong bộ nhớ (sử dụng dict để tra cứu O(1) theo label).
    - Quản lý các phiên bản chỉ mục (LinearScan, KDTree, LSH, IVF, HNSW) và tự động cập nhật khi dữ liệu thay đổi.
    - Quản lý ngăn xếp `LinkedStack` lưu các `ActionRecord` để thực thi cơ chế Hoàn tác (Undo).
    - Cung cấp API nội bộ cho tầng UI (`src.ui`):
        + `add_record(label, vector)`
        + `delete_record(label)`
        + `undo()`
        + `search_and_benchmark(query_word, k, metric)`
"""
