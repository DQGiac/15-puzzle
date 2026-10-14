"""
Module định nghĩa các hàm tính toán độ đo khoảng cách và độ tương đồng giữa các vector.

Tác dụng trong dự án:
    - Cung cấp 2 độ đo chính:
        + Cosine Distance: $1 - \\frac{u \\cdot v}{\\|u\\| \\cdot \\|v\\|}$ (tận dụng thuộc tính `_norm` tính sẵn của VectorRecord để tăng tốc).
        + Euclidean Distance ($L_2$): $\\sqrt{\\sum_{i=1}^{d} (u_i - v_i)^2}$.
    - Ràng buộc: Tự cài đặt bằng toán học thuần túy (vòng lặp, phép nhân, căn bậc hai với module `math`), không dùng NumPy hay Scipy.
"""
