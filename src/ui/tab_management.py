"""
Giao diện Tab 1: Quản lý dữ liệu vector (vai trò tương tự Milvus thu nhỏ).

Tác dụng trong dự án:
    - Hiển thị danh sách các từ vựng và vector hiện có trong hệ thống (dạng bảng/phân trang).
    - Cung cấp form thêm từ mới (nhập nhãn từ và 50 giá trị thực của vector).
    - Cung cấp nút xóa từ vựng được chọn khỏi cơ sở dữ liệu.
    - Cung cấp nút 'Hoàn tác' (Undo) để khôi phục thao tác thêm/xóa gần nhất thông qua LinkedStack.
"""
import random
import math
import streamlit as st

def _generate_random_vector(dim: int = 50) -> list[float]:
    """Sinh vector 50 chiều ngẫu nhiên chuẩn hóa."""
    vec = [round(random.uniform(-1.0, 1.0), 4) for _ in range(dim)]
    norm = math.sqrt(sum(x * x for x in vec))
    return [round(x / (norm if norm != 0 else 1.0), 4) for x in vec]

def _init_mock_data():
    """Khởi tạo tập từ vựng mẫu ban đầu nếu session_state chưa có."""
    if "vector_db" not in st.session_state:
        sample_words = [
            "king", "queen", "prince", "princess", "palace",
            "vietnam", "hanoi", "danang", "saigon", "asia",
            "computer", "software", "algorithm", "python", "matrix",
            "doctor", "hospital", "nurse", "medicine", "health",
            "cat", "dog", "tiger", "lion", "animal",
            "apple", "banana", "orange", "mango", "fruit"
        ]
        db = {}
        for w in sample_words:
            vec = _generate_random_vector(50)
            norm = round(math.sqrt(sum(x * x for x in vec)), 4)
            db[w] = {
                "label": w,
                "dimension": 50,
                "norm": norm,
                "preview": f"[{vec[0]:.3f}, {vec[1]:.3f}, {vec[2]:.3f}, ..., {vec[-1]:.3f}]",
                "vector": vec
            }
        st.session_state.vector_db = db

    if "undo_stack" not in st.session_state:
        st.session_state.undo_stack = []

def render_tab1_management():
    """
    Render Giao diện Tab 1: Quản lý dữ liệu vector (Mô phỏng Milvus thu nhỏ)
    Thiết kế bám sát sơ đồ: docs/images/ui_tab1_management.png
    """
    _init_mock_data()
    db = st.session_state.vector_db
    undo_stack = st.session_state.undo_stack

    st.header("📁 Quản lý Dữ liệu Vector", divider="rainbow")
    st.caption("Quản trị cơ sở dữ liệu vector: Nạp dữ liệu, Xem danh sách, Thêm, Xóa và Hoàn tác (Undo).")

    # -------------------------------------------------------------------------
    # 1. THÔNG SỐ TỔNG QUAN (Metrics)
    # -------------------------------------------------------------------------
    st.subheader("1. Thông số tổng quan", divider="blue")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label=":blue[Tổng số từ vựng (N)]", value=len(db))
    with col2:
        st.metric(label=":green[Số chiều (d)]", value="50 (GloVe)")
    with col3:
        st.metric(label=":orange[Số thao tác trong Stack Undo]", value=len(undo_stack))
    with col4:
        st.metric(label=":rainbow[Trạng thái Chỉ mục (Index)]", value="Đồng bộ")

    st.write("")

    # -------------------------------------------------------------------------
    # 2. NẠP DỮ LIỆU
    # -------------------------------------------------------------------------
    st.subheader("2. Nạp dữ liệu", divider="blue")
    col_load1, col_load2 = st.columns([2, 1], gap="medium")
    with col_load1:
        row_choice = st.radio(
            "Chọn số dòng dữ liệu nạp từ tập GloVe:",
            options=[100, 500, 1000, 5000],
            index=0,
            horizontal=True,
            help="Tải trước một lượng vector vào bộ nhớ để thử nghiệm quy mô"
        )
    with col_load2:
        st.write("")
        st.write("")
        if st.button("📥 Nạp dữ liệu mẫu có sẵn", type="primary", use_container_width=True):
            # Tạo số lượng từ tương ứng
            new_db = dict(db)
            for i in range(len(new_db) + 1, row_choice + 1):
                w = f"word_{i}"
                vec = _generate_random_vector(50)
                norm = round(math.sqrt(sum(x * x for x in vec)), 4)
                new_db[w] = {
                    "label": w,
                    "dimension": 50,
                    "norm": norm,
                    "preview": f"[{vec[0]:.3f}, {vec[1]:.3f}, ..., {vec[-1]:.3f}]",
                    "vector": vec
                }
            st.session_state.vector_db = new_db
            st.success(f"Đã nạp thành công {row_choice} từ vựng vào hệ thống!")
            st.rerun()

    st.write("")

    # -------------------------------------------------------------------------
    # 3. BẢNG TỪ VỰNG (Nhãn, Tọa độ vector, Norm)
    # -------------------------------------------------------------------------
    st.subheader("3. Bảng từ vựng trong cơ sở dữ liệu", divider="blue")
    
    col_search, col_count = st.columns([3, 1])
    with col_search:
        filter_query = st.text_input("🔍 Lọc từ vựng theo tên:", placeholder="Nhập từ cần tìm trong bảng (ví dụ: king, vietnam...)")
    with col_count:
        st.write("")
        st.caption(f"Đang hiển thị {len(db)} bản ghi")

    # Chuẩn bị dữ liệu hiển thị
    display_rows = []
    for record in db.values():
        if not filter_query or filter_query.lower() in record["label"].lower():
            display_rows.append({
                "Từ vựng (Label)": record["label"],
                "Số chiều": record["dimension"],
                "Độ dài Norm (L2)": record["norm"],
                "Vector Preview (50D)": record["preview"]
            })

    st.dataframe(
        display_rows,
        use_container_width=True,
        hide_index=True,
        height=280
    )

    st.write("")

    # -------------------------------------------------------------------------
    # 4. THAO TÁC: THÊM TỪ VỰNG MỚI, XÓA TỪ & HOÀN TÁC (UNDO)
    # -------------------------------------------------------------------------
    st.subheader("4. Thao tác dữ liệu & Hoàn tác", divider="blue")
    col_add, col_del = st.columns(2, gap="large")

    # --- Thêm từ vựng mới (Biểu mẫu) ---
    with col_add:
        st.markdown("**➕ Thêm từ vựng mới (Biểu mẫu)**")
        with st.form("form_add_word", clear_on_submit=True):
            new_label = st.text_input("Nhãn từ vựng (Word Label):", placeholder="Ví dụ: artificial_intelligence")
            generate_auto = st.checkbox("Tự động sinh ngẫu nhiên vector 50 chiều", value=True)
            custom_vec_str = st.text_area(
                "Hoặc nhập 50 giá trị cách nhau bằng dấu cách/phẩy:",
                placeholder="0.12 -0.34 0.56 ...",
                disabled=generate_auto
            )
            submit_add = st.form_submit_button("Thêm vào hệ thống", type="primary", use_container_width=True)

        if submit_add:
            label_clean = new_label.strip().lower()
            if not label_clean:
                st.error("Vui lòng nhập nhãn từ!")
            elif label_clean in db:
                st.warning(f"Từ '{label_clean}' đã tồn tại trong cơ sở dữ liệu!")
            else:
                if generate_auto:
                    vec = _generate_random_vector(50)
                else:
                    try:
                        vals = [float(x.strip()) for x in custom_vec_str.replace(",", " ").split() if x.strip()]
                        if len(vals) != 50:
                            st.error(f"Vector cần đúng 50 số! Hiện có {len(vals)} số.")
                            st.stop()
                        vec = vals
                    except ValueError:
                        st.error("Dữ liệu vector không hợp lệ!")
                        st.stop()

                norm = round(math.sqrt(sum(x * x for x in vec)), 4)
                # Lưu vào database
                db[label_clean] = {
                    "label": label_clean,
                    "dimension": 50,
                    "norm": norm,
                    "preview": f"[{vec[0]:.3f}, {vec[1]:.3f}, ..., {vec[-1]:.3f}]",
                    "vector": vec
                }
                # Lưu lịch sử vào Stack Undo: loại 'ADD'
                undo_stack.append({
                    "action": "ADD",
                    "label": label_clean,
                    "payload": None
                })
                st.success(f"Đã thêm thành công từ '{label_clean}'!")
                st.rerun()

    # --- Xóa từ vựng & Nút Hoàn tác ---
    with col_del:
        st.markdown("**🗑️ Xóa từ vựng theo tên**")
        word_to_delete = st.selectbox(
            "Chọn từ vựng muốn xóa khỏi CSDL:",
            options=[""] + sorted(list(db.keys())),
            help="Chọn từ trong danh sách hiện tại"
        )
        if st.button("Xóa từ vựng này", use_container_width=True):
            if word_to_delete and word_to_delete in db:
                removed_record = db.pop(word_to_delete)
                # Lưu vết vào Stack Undo: loại 'DELETE' kèm payload để khôi phục
                undo_stack.append({
                    "action": "DELETE",
                    "label": word_to_delete,
                    "payload": removed_record
                })
                st.warning(f"Đã xóa từ '{word_to_delete}' khỏi hệ thống!")
                st.rerun()
            else:
                st.error("Vui lòng chọn từ hợp lệ để xóa!")

        st.write("")
        st.markdown("**↩️ Hoàn tác (Undo từ LinkedStack)**")
        st.caption("Khôi phục lại thao tác thêm hoặc xóa từ vựng gần nhất.")
        
        if st.button("🔄 Hoàn tác thao tác gần nhất (Undo)", type="primary", use_container_width=True):
            if not undo_stack:
                st.info("Ngăn xếp Undo rỗng, không có thao tác nào để hoàn tác!")
            else:
                last_action = undo_stack.pop()
                action_type = last_action["action"]
                action_label = last_action["label"]

                if action_type == "ADD":
                    # Hoàn tác việc thêm: Xóa từ đã thêm
                    if action_label in db:
                        del db[action_label]
                    st.success(f"Hoàn tác: Đã hủy thao tác thêm từ '{action_label}'!")
                elif action_type == "DELETE":
                    # Hoàn tác việc xóa: Thêm lại từ đã xóa
                    payload = last_action["payload"]
                    if payload:
                        db[action_label] = payload
                    st.success(f"Hoàn tác: Đã khôi phục lại từ '{action_label}'!")
                st.rerun()
