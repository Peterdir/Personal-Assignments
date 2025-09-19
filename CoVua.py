# N-Queens GUI with BFS/DFS/UCS (mobility-based cost, cost chỉ hiện khi UCS)
# ======================
# Import
# ======================
from queue import Queue, PriorityQueue
from tkinter import *
import os
import math
from PIL import Image, ImageTk

# ======================
# Khởi tạo Tkinter
# ======================
root = Tk()
root.geometry("1300x725+10+10")
root.title("Cờ vua Việt - UCS mobility cost")

C1 = Canvas(root, bg="white", height=540, width=540)
C1.place(x=50, y=30)

C2 = Canvas(root, bg="white", height=540, width=540)
C2.place(x=650, y=30)

# ======================
# Biến toàn cục
# ======================
size = 62.5
N = 8
offset = 30
size_col = 10
current_path = []
current_index = 0
cost_map = {}  # Lưu chi phí
is_running = False
current_algo = None

# Thời gian giữa các bước chạy trên C!
step_delay = 200
dfs_gen = None  # biến toàn cục để lưu generator
# Danh sách trạng thái 

# ======================
# Hàm vẽ bàn cờ & tiện ích
# ======================
def clear_queens():
    global current_path, current_index, is_running, cost_map, current_algo
    is_running = False
    current_path = []
    current_index = 0
    cost_map = {}
    current_algo = None

    C1.delete("all")
    draw_labels(C2)
    for i in range(N):
        for j in range(N):
            x1 = size * i + offset
            y1 = size * j
            x2 = x1 + size
            y2 = y1 + size
            color = "#873e23" if (i + j) % 2 == 0 else "#eab676"
            C1.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
    cost_label.config(text="")

    C2.delete("all")
    draw_labels(C2)
    for i in range(N):
        for j in range(N):
            x1 = size * i + offset
            y1 = size * j
            x2 = x1 + size
            y2 = y1 + size
            color = "#873e23" if (i + j) % 2 == 0 else "#eab676"
            C2.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
    cost_label.config(text="")

def draw_labels(canvas):
    cols = ['1','2','3','4','5','6','7','8']
    rows = ['A','B','C','D','E','F','G','H']
    for i in range(N):
        y = size * i + size / 2
        canvas.create_text(size_col, y, text=cols[i], font=("Arial", 12, "bold"))
    for i in range(N):
        x = size * i + offset + size / 2
        canvas.create_text(x, N * size + 15, text=rows[i], font=("Arial", 12, "bold"))

def table_initial():
    C1.delete("all")
    for i in range(N):
        for j in range(N):
            x1 = size * i + offset
            y1 = size * j
            x2 = x1 + size
            y2 = y1 + size
            color = "#873e23" if (i + j) % 2 == 0 else "#eab676"
            C1.create_rectangle(x1, y1, x2, y2, fill=color)


def table_operator():
    C2.delete("all")
    for i in range(N):
        for j in range(N):
            x1 = size * i + offset
            y1 = size * j
            x2 = x1 + size
            y2 = y1 + size
            color = "#873e23" if (i + j) % 2 == 0 else "#eab676"
            C2.create_rectangle(x1, y1, x2, y2, fill=color)

# ======================
# Thuật toán chung
# ======================
def check_queens(state, col):
    row = len(state)
    for r in range(row):
        c = state[r]
        if c == col or abs(r - row) == abs(c - col):
            return False
    return True

def reconstruct_path(parent, state_tuple):
    path = []
    s = state_tuple
    while s is not None:
        path.append(list(s))
        s = parent.get(s)
    return path[::-1]

# ======================
# Mobility / cost functions
# ======================
def occupied_positions(state):
    return {(r, c) for r, c in enumerate(state)}

DIRECTIONS = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

def mobility_of_queen(state, row, col):
    occ = occupied_positions(state)
    count = 0
    for dr, dc in DIRECTIONS:
        r, c = row+dr, col+dc
        while 0 <= r < N and 0 <= c < N:
            if (r, c) in occ:
                break
            count += 1
            r += dr
            c += dc
    return count

def cost_of_state(state):
    total = 0
    for r, c in enumerate(state):
        total += mobility_of_queen(state, r, c)
    return total

# ======================
# Cost function for Informed (Heuristic) Search Strategies
# ====================== 
GOAL_STATE = [1, 3, 5, 7, 2, 0, 6, 4]
def is_goal(state):
    global GOAL_STATE
    return state == GOAL_STATE

def heuristic(state):
    total = 0
    for row in range(len(state)):
        total += abs(state[row] - GOAL_STATE[row])
    
    return total

def greedy_best_first_search():
    global N
    start = []
    frontier = PriorityQueue()
    frontier.put((heuristic(start), start))
    parent = {tuple(start): None}

    while not frontier.empty():
        h_val, state = frontier.get()

        if is_goal(state):
            return reconstruct_path(parent, tuple(state))
        
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                if tuple(new_state) not in parent:
                    parent[tuple(new_state)] = tuple(state)
                    frontier.put((heuristic(new_state), new_state))

    return []

# ======================
# DLS (Depth - limited search)
# ======================
def iterative_deepening_search(N):
    for depth in range(N + 1):
        result = depth_limited_search(N, depth)
        if result != "cutoff":
            return result

def depth_limited_search(N, limit):
    start = []
    parent = {tuple(start): None}
    return recursive_DLS(start, parent, N, limit)

def recursive_DLS(state, parent, N, limit):
    if len(state) == N:
        return reconstruct_path(parent, tuple(state))
    elif limit == 0:
        return "cutoff"
    else:
        cutoff_occurred = False
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                if tuple(new_state) not in parent:
                    parent[tuple(new_state)] = tuple(state)
                result = recursive_DLS(new_state, parent, N, limit - 1)
                if result == "cutoff":
                    cutoff_occurred = True
                elif result != "failure":
                    return result 
        if cutoff_occurred:
            return "cutoff"
        else:
            return "failure"

# ======================
# UCS (Uniform - cost search)
# ======================
def uniform_cost_search(N):
    start = []
    frontier = PriorityQueue()
    frontier.put((cost_of_state(start), start))
    parent = {tuple(start): None}
    cost_so_far = {tuple(start): cost_of_state(start)}

    while not frontier.empty():
        path_cost, state = frontier.get()
        tstate = tuple(state)
        if cost_so_far.get(tstate) != path_cost:
            continue
        if len(state) == N:
            return reconstruct_path(parent, tstate), cost_so_far
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                new_cost = cost_of_state(new_state)
                tnew = tuple(new_state)
                if tnew not in cost_so_far or new_cost < cost_so_far[tnew]:
                    cost_so_far[tnew] = new_cost
                    parent[tnew] = tstate
                    frontier.put((new_cost, new_state))
    return [], cost_so_far

# ======================
# DFS / BFS
# ======================
def dfs_queens(N):
    stack = [[]]
    parent = {tuple([]): None}
    while stack:
        state = stack.pop()
        tstate = tuple(state)
        if len(state) == N:
            return [reconstruct_path(parent, tstate)]
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                tnew = tuple(new_state)
                if tnew not in parent:
                    parent[tnew] = tstate
                    stack.append(new_state)
    return []

def bfs_queens(N):
    def actions(state): return [col for col in range(N) if check_queens(state, col)]
    def child_node(state, action): return state + [action]
    node = []
    frontier = Queue()
    frontier.put(node)
    parent = {tuple(node): None}
    while not frontier.empty():
        state = frontier.get()
        for action in actions(state):
            child = child_node(state, action)
            tchild = tuple(child)
            if tchild not in parent:
                parent[tchild] = tuple(state)
                if len(child) == N:
                    return [reconstruct_path(parent, tchild)]
                frontier.put(child)
    return []

# ======================
# A* Search
# ======================
def astar_search(N):
    """
    A*: sử dụng g = cost_of_state(state) và h = heuristic(state)
    Trả về (path, cost_map) giống kiểu của UCS: path là danh sách trạng thái từ start->goal,
    cost_map lưu giá trị g (cost_of_state) của từng trạng thái được thăm/ghi nhận.
    """
    start = []
    frontier = PriorityQueue()
    g_start = cost_of_state(start)
    f_start = g_start + heuristic(start)
    frontier.put((f_start, g_start, start))
    parent = {tuple(start): None}
    cost_so_far = {tuple(start): g_start}

    while not frontier.empty():
        f_val, g_val, state = frontier.get()
        tstate = tuple(state)
        # Bỏ những entry cũ không khớp với chi phí hiện tại
        if cost_so_far.get(tstate, None) != g_val:
            continue

        # Goal test: khi đạt đủ N hàng (hoặc so sánh với GOAL_STATE tuỳ bạn)
        if len(state) == N:
            return reconstruct_path(parent, tstate), cost_so_far

        # Expand
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                tnew = tuple(new_state)
                new_g = cost_of_state(new_state)  # theo cách bạn dùng ở UCS
                # Nếu chưa thấy hoặc tìm được chi phí g nhỏ hơn -> cập nhật
                if tnew not in cost_so_far or new_g < cost_so_far[tnew]:
                    cost_so_far[tnew] = new_g
                    parent[tnew] = tstate
                    new_f = new_g + heuristic(new_state)
                    frontier.put((new_f, new_g, new_state))

    return [], cost_so_far

# ======================
# Generator
# ======================
def dfs_generator(N):
    stack = [[]]  # bắt đầu từ trạng thái rỗng
    parent = {tuple([]): None}
    while stack:
        state = stack.pop()
        yield ("visit", state)  # báo là đang thăm trạng thái này
        if len(state) == N:  # nếu tìm thấy lời giải
            yield ("found", tuple(state), parent)
            return
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                tnew = tuple(new_state)
                if tnew not in parent:
                    parent[tnew] = tuple(state)
                    stack.append(new_state)
                    yield ("push", new_state)  # báo là thêm trạng thái mới vào stack

# ======================
# Hiển thị trạng thái
# ======================
def draw_state(state):
    # vẽ final state lên C2
    if current_algo == "UCS":
        tstate = tuple(state)
        cost = cost_map.get(tstate, cost_of_state(state))
        draw_state_on_canvas(C2, state, show_mobility=True, show_cost=cost)
        cost_label.config(text=f"Cost: {cost}")
    else:
        draw_state_on_canvas(C2, state, show_mobility=False, show_cost=None)
        cost_label.config(text="")

def draw_state_on_canvas(canvas, state, show_mobility=False, show_cost=None):
    # Vẽ bàn
    canvas.delete("all")
    draw_labels(canvas)
    for i in range(N):
        for j in range(N):
            x1 = size * i + offset
            y1 = size * j
            x2 = x1 + size
            y2 = y1 + size
            color = "#873e23" if (i + j) % 2 == 0 else "#eab676"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
    
    # vẽ hậu & mobility (nếu yêu cầu)
    for row, col in enumerate(state):
        x1 = size*col+offset
        y1 = size*row
        x2, y2 = x1+size, y1+size
        try:
            canvas.create_image((x1+x2)/2, (y1+y2)/2, image=queen_img)
        except:
            canvas.create_text((x1+x2)/2, (y1+y2)/2, text='Q', font=("Arial", 24, "bold"))
        if show_mobility:
            mob = mobility_of_queen(state, row, col)
            canvas.create_text(x1+8, y1+10, text=str(mob), anchor="nw",
                               font=("Arial", 10, "bold"), fill="white")
        
    # Nếu yêu cầu hiển thị cost (dùng cho C2 khi UCS)
    if show_cost is not None:
        canvas.create_text(250, 560, text=f"Cost: {show_cost}", font=("Arial", 14, "bold"), fill="blue")
        


# ======================
# Auto-run
# ======================
def show_next_state():
    global current_index
    if current_index < len(current_path):
        draw_state_on_canvas(C1, current_path[current_index], show_mobility=True, show_cost=None)
        current_index += 1

def resume_run():
    global is_running
    is_running = True
    run_next_state()

def stop_run():
    global is_running
    is_running = False

def run_next_state():
    global current_index, is_running
    if is_running and current_index < len(current_path):
        show_next_state()
        root.after(step_delay, run_next_state)

def run_dfs_auto():
    global dfs_gen, current_algo, is_running
    # 1. Tìm nghiệm hoàn chỉnh bằng dfs_queens()
    solutions = dfs_queens(N)
    if solutions:
        final_solution = solutions[0][-1]  # lấy state cuối cùng trong nghiệm
        draw_state_on_canvas(C2, final_solution, show_mobility=False)  # vẽ ngay nghiệm bên phải
    
    # 2. Sau đó mới khởi động generator để chạy step-by-step cho C1
    dfs_gen = dfs_generator(N)
    current_algo = "DFS"
    is_running = True
    run_dfs_step()

def run_bfs_auto():
    global current_path, current_index, is_running, current_algo
    solutions = bfs_queens(N)
    if solutions:
        current_algo = "BFS"
        current_path = solutions[0]
        current_index = 0
        is_running = True
        run_next_state()

def run_ucs_auto():
    global current_path, current_index, cost_map, is_running, current_algo
    path, cmap = uniform_cost_search(N)
    cost_map = cmap
    if path:
        current_algo = "UCS"
        current_path = path
        current_index = 0
        is_running = True
        run_next_state()

def run_dls_auto():
    global current_path, current_index, is_running, current_algo
    solutions = depth_limited_search(N, 8)
    if solutions:
        current_algo = "DLS"
        current_path = solutions
        current_index = 0
        is_running = True
        run_next_state()

def run_ids_auto():
    global current_path, current_index, is_running, current_algo
    solutions = iterative_deepening_search(N)
    if solutions:
        current_algo = "Iterative deepening search"
        current_path = solutions
        current_index = 0
        is_running = True
        run_next_state()

def run_gbfs_auto():
    global current_path, current_index, is_running, current_algo
    solutions = greedy_best_first_search()
    if solutions:
        current_algo = "Greedy best-first search"
        current_path = solutions
        current_index = 0
        is_running = True
        run_next_state()

def run_astar_auto():
    global current_path, current_index, cost_map, is_running, current_algo
    path, cmap = astar_search(N)
    cost_map = cmap
    if path:
        current_algo = "A*"
        current_path = path
        current_index = 0
        is_running = True
        run_next_state()

# ======================
# Step-by-step
# ======================
def run_dfs_step():
    global dfs_gen, is_running
    if not is_running:
        return
    try:
        event = next(dfs_gen)
        if event[0] in ("visit", "push"):
            state = event[1]
            # Vẽ trạng thái tạm thời bên trái (C1)
            draw_state_on_canvas(C1, state, show_mobility=False)
        elif event[0] == "found":
            final_state = list(event[1])
            # Vẽ nghiệm cuối cùng bên phải (C2)
            draw_state_on_canvas(C2, final_state, show_mobility=False)
            is_running = False
            return
        root.after(step_delay, run_dfs_step)
    except StopIteration:
        is_running = False


# ======================
# Load ảnh hậu
# ======================
current_dir = os.path.dirname(os.path.abspath(__file__))
queen_path = os.path.join(current_dir, "wq.png")
try:
    try:
        resample = Image.Resampling.LANCZOS
    except:
        resample = Image.LANCZOS
    img = Image.open(queen_path).resize((int(size), int(size)), resample)
    queen_img = ImageTk.PhotoImage(img)
except:
    queen_img = PhotoImage(width=int(size), height=int(size))

# ======================
# Giao diện nút
# ======================
table_initial()
table_operator()
draw_labels(C1)
draw_labels(C2)

btn_frame = Frame(root, bg="white")
btn_frame.pack(side=BOTTOM, pady=10)

Button(btn_frame,text="🌐 BFS",font=("Arial",14,"bold"),
       bg="#009688",fg="white",command=run_bfs_auto).grid(row=0,column=0,padx=10,pady=10)
Button(btn_frame,text="🌲 DFS",font=("Arial",14,"bold"),
       bg="#795548",fg="white",command=run_dfs_auto).grid(row=0,column=1,padx=10,pady=10)
Button(btn_frame,text="💰 UCS",font=("Arial",14,"bold"),
       bg="#3F51B5",fg="white",command=run_ucs_auto).grid(row=0,column=2,padx=10,pady=10)
Button(btn_frame,text="DLS",font=("Arial",14,"bold"),
       bg="#9E9E9E",fg="white",command=run_dls_auto).grid(row=0,column=3,padx=10,pady=10)
Button(btn_frame,text="Iterative deepening DFS",font=("Arial",14,"bold"),
       bg="#9E9E9E",fg="white",command=run_ids_auto).grid(row=0,column=4,padx=10,pady=10)
Button(btn_frame,text="Greedy best-first search",font=("Arial",14,"bold"),
       bg="#9E9E9E",fg="white",command=run_gbfs_auto).grid(row=0,column=5,padx=10,pady=10)
Button(btn_frame,text="A* Search",font=("Arial",14,"bold"),
       bg="#FF9800",fg="white",command=run_astar_auto).grid(row=0,column=6,padx=10,pady=10)
Button(btn_frame,text="⏯ Resume",font=("Arial",14,"bold"),
       bg="#4CAF50",fg="white",command=resume_run).grid(row=0,column=7,padx=10,pady=10)
Button(btn_frame,text="⏸ Stop",font=("Arial",14,"bold"),
       bg="#F44336",fg="white",command=stop_run).grid(row=0,column=8,padx=10,pady=10)
Button(btn_frame,text="🧹 Clear",font=("Arial",14,"bold"),
       bg="#9E9E9E",fg="white",command=clear_queens).grid(row=0,column=9,padx=10,pady=10)

for i in range(10):
    btn_frame.grid_columnconfigure(i, weight=1)

cost_label = Label(root, text="", font=("Arial",14), fg="blue")
cost_label.pack(pady=5)

# ======================
# Main loop
# ======================
root.mainloop()
