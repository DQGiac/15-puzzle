THIẾT KẾ HỆ THỐNG DỰ ÁN 15-PUZZLE
Project 1 giới thiệu
Trò chơi bao gồm một khung hình vuông 4 × 4 chứa 15 ô vuông được đánh số từ 1 đến 15, và một vị trí trống. Người chơi chỉ được phép trượt các ô kề cạnh ô trống vào vị trí ô trống (tương đương với việc “di chuyển” ô trống theo 4 hướng: lên, xuống, trái, phải). Mục tiêu là biến đổi từ trạng thái ban đầu (bị xáo trộn) về trạng thái đích:  

1. Luồng hoạt động hệ thống

-       Khởi tạo (Init): Sinh ma trận 4x4 theo thứ tự đã giải, sau đó tự động xáo ngẫu nhiên 50 bước ngược để đảm bảo bàn cờ luôn ở trạng thái giải được 100%, có thể đọc 1 input bên ngoài đương nhiên phải kiểm tra có giải được hay không.
-       Tương tác (Input): Hệ thống lắng nghe sự kiện từ người dùng. Các thao tác hợp lệ bao gồm click chuột vào ô kề khoảng trống, nhấn phím SPACE để kích hoạt AI giải tự động, S/L để Lưu/Tải trạng thái, và R để tạo ván mới (hoặc click chuột vào các nút chức năng trên màn hình).
-       Kết thúc (Endgame): Kiểm tra trạng thái ma trận có khớp thứ tự 1 -> 15 hay không. Cập nhật dữ liệu người chơi vào ScoreRecord.

1. Cấu trúc dữ liệu
Các cấu trúc dữ liệu dự định sử dụng:

-       Ma trận 2D: Mảng tĩnh Tile grid[4][4] để biểu diễn lưới không gian 16 ô cờ.
-      Mảng động (Vector): Quản lý các danh sách biến đổi kích thước liên tục (như lịch sử di chuyển hoặc danh sách các nút trên cây tìm kiếm). 
-     Bảng băm (HashTable): Dùng chứa các trạng thái bàn cờ đã được thuật toán AI duyệt qua và kiểm tra trạng thái đó đã từng duyệt qua hay chưa. Nếu đã duyệt qua rồi thì cắt.

1. Thiết kế Hướng đối tượng (OOP)

-       Tile: Lưu trữ value (giá trị từ 0-15) và tọa độ pixel_x, pixel_y của từng mảnh trong bảng.
-      Board / GameEngine: Quản lý lưới và xử lý logic. Chứa phương thức kiểm tra tính giải được dựa trên công thức toán học: (N_inv + R_blank) % 2 == 1.
-     AI_Solver: Lớp xử lý thuật toán tách biệt. Cài đặt thuật toán IDA* (Iterative Deepening A*) với hàm đánh giá chi phí heuristics là f = g + 2*h (trong đó h là khoảng cách Manhattan). Lớp sử dụng HashTable để loại bỏ trạng thái trùng lặp.
-       ScoreRecord: Chứa thông tin của một lượt chơi xuất sắc bao gồm tên, số bước và thời gian. 

1. Thuật toán
Thuật toán AI tự động giải trong hệ thống được triển khai dựa trên IDA*(Iterative Deepening A*), kết hợp ưu điểm của tìm kiếm theo chiều sâu (DFS) về mặt tiết kiệm bộ nhớ và thuật toán A* trong việc tìm đường đi ngắn nhất.

-      Hàm đánh giá Heuristic: Sử dụng công thức f = g + 2*h, trong đó g là chi phí (số bước đi) từ trạng thái ban đầu và h là tổng khoảng cách Manhattan của các ô cờ về vị trí đích. Việc nhân hệ số 2 vào h giúp gia tăng trọng số heuristic, thúc đẩy AI tìm kiếm nhanh hơn và ưu tiên các nhánh tiệm cận đích.
-       Cách thức hoạt động: Thuật toán thực hiện quay lùi (backtracking) với một ngưỡng chi phí f_limit cố định. Ở mỗi chu kỳ, nếu giá trị f vượt quá f_limit, đường đi đó sẽ bị ngắt. Ngưỡng f_limit sẽ được cập nhật liên tục bằng giá trị f nhỏ nhất bị vượt ngưỡng từ lượt tìm kiếm trước cho đến khi tìm thấy trạng thái đích.
-       Tối ưu hóa bằng Bảng băm (HashTable): Để tránh duyệt lại các trạng thái trùng lặp hoặc lặp vòng vô hạn trên cùng một nhánh, ma trận bàn cờ được băm thành mã định danh duy nhất và lưu vào HashTable. Khi sinh trạng thái mới, hệ thống sẽ tra cứu nhanh trong HashTable để loại bỏ ngay các trạng thái đã từng duyệt.

Có thể so sánh với thuật toán A* về thời gian, bộ nhớ.
5. Thiết kế Cơ sở dữ liệu (Storage)
Dự án chạy trên máy cục bộ, database sẽ được triển khai dưới dạng tệp dat.

-       Lưu trữ bảng xếp hạng (Leaderboard): Bảng này lưu trữ thông tin các lượt chơi theo định dạng CSV.
-       Lưu trữ trạng thái ván đấu file save.dat (hoặc biến trạng thái tạm) giữ nguyên ảnh chụp của bàn cờ hiện tại. Nội dung lưu bao gồm cấu trúc mảng 16 số hiện hành, số bước người chơi đã đi và bộ đếm thời gian đang dừng.
