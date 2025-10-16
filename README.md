# 📖 Bài toán (Problem Definition)
>Đây là chương trình trực quan hóa bài toán 8 quân hậu được xây dựng với ngôn ngữ python bằng thư viện Tkinter.
>Mục tiêu của bài toán là đặt 8 quân hậu vào bàn cờ kích thước 8x8 sao cho không có quân hậu nào ăn lẫn nhau.

## 🧠 Giao diện (Interface)
>Phần mềm được xây dựng bằng Python - Tkinter, hỗ trợ:
- **2 bàn cờ song song**:  
  - Bên trái (**C1**): hiển thị quá trình thuật toán duyệt từng trạng thái.  
  - Bên phải (**C2**): hiển thị lời giải cuối cùng.  
- **Thanh nút chức năng**:  
  - **Nhóm thuật toán tìm kiếm cổ điển (Classical Search)**  
    - **BFS**  
    - **DFS**  
    - **UCS** (có hiển thị *mobility-based cost*)  
    - **DLS**  
    - **IDS**  
  - **Nhóm thuật toán heuristic (Informed Search)**  
    - **Greedy Best-First Search**  
    - **A\* Search**  
    - **Hill Climbing**  
    - **Simulated Annealing**  
  - **Nhóm local search nâng cao & điều khiển**  
    - **Local Beam Search**  
    - **Genetic Algorithm**  
- **Nhóm thuật toán CSP / ràng buộc (Constraint Satisfaction Problem)**  
    - **Backtracking Search**  
    - **Forward Checking**  
    - **AC-3 (Arc Consistency #3)**  
  - **Nhóm nâng cao / điều khiển**  
    - **AND-OR Search**  
    - **Sensorless Search (No Observation)**  
    - **Partial Observable Search**  
    - ⏯ **Resume** (tiếp tục chạy)  
    - ⏸ **Stop** (dừng chạy)  
    - 🧹 **Clear** (xóa bàn cờ, reset trạng thái)  
- **Thanh thông tin Cost**: hiển thị chi phí lời giải (*dành cho UCS/A\**).

## 🔍 Các thuật toán đã hỗ trợ  
### Thuật toán tìm kiếm không thông tin (Uninformed Search)  
- Breadth-First Search (BFS)  
- Depth-First Search (DFS)  
- Uniform Cost Search (UCS)  
- Depth-Limited Search (DLS)  
- Iterative Deepening Search (IDS)  

### Thuật toán tìm kiếm có thông tin (Informed Search)  
- Greedy Best-First Search (GBFS)  
- A* Search  

### Thuật toán tối ưu / Local Search  
- Hill Climbing  
- Simulated Annealing  
- Local Beam Search  
- Genetic Algorithm

### 4️⃣ Thuật toán CSP (Constraint Satisfaction Problem)  
- Backtracking Search  
- Forward Checking  
- AC-3 (Arc Consistency #3)  

### 5️⃣ Thuật toán nâng cao  
- AND-OR Search  
- Sensorless Search (No Observation)  
- Partial Observable Search  

## 💻 Cách chạy chương trình
>Yêu cầu:
* Python 3.x đã được cài đặt
* Cài đặt Visual studio code
* Cài extension của python trên Visual studio code
>Chạy chương trình:
* Mở file Python bằng Visual studio code.
* Ấn tổ hợp phím (Ctrl + Shift + P), sau đó tìm và chọn Select Interpreter để chọn phiên bản python phù hợp.
* Nhấn f5 sau đó chọn Python Debugger, chọn Python file.
* Sau khi chạy thành công, phần mềm sẽ hiện thị **giao diện bàn cờ 8x8** cùng với các **chức năng có trong phần mềm**.

## ✍️ Tác giả
>Họ tên: Lâm Khánh Duy
>
>Mã số sinh viên: 23110084

## ⭐ Lời cảm ơn & Tài liệu tham khảo
>Em chân thành cảm ơn giảng viên Phan Thị Huyền Trang đã tận tình giảng dạy, truyền đạt và hướng dẫn em, giúp em hoàn thành bài tập cá nhân này.
>
>Tài liệu tham khảo:
* Python Tkinter Tutorial: https://www.geeksforgeeks.org/python/python-tkinter-tutorial/
* Python documentation: https://docs.python.org/3/
* Russell 2016 Artificial intelligence a modern approach - Stuart Russell và Peter Norvig