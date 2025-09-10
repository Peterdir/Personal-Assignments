# N-Queens GUI with BFS/DFS/UCS (mobility-based cost, cost chỉ hiện khi UCS)
# ======================
# Import
# ======================
from queue import Queue, PriorityQueue
from tkinter import *
import os
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
cost_map = {}      # lưu chi phí từ UCS
is_running = False
current_algo = None   # "BFS", "DFS", "UCS"

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
# UCS
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
        for col in range(N-1, -1, -1):
            if check_queens(state, col):
                new_state = state + [col]
                tnew = tuple(new_state)
                if tnew not in parent:
                    parent[tnew] = tstate
                    stack.append(new_state)
    return []

def bfs_queens(N):
    def goal_test(state): return len(state) == N
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
                if goal_test(child):
                    return [reconstruct_path(parent, tchild)]
                frontier.put(child)
    return []

# ======================
# Hiển thị trạng thái
# ======================
def draw_state(state):
    C2.delete("all")
    draw_labels(C2)
    # vẽ bàn
    for i in range(N):
        for j in range(N):
            x1, y1 = size*i+offset, size*j
            x2, y2 = x1+size, y1+size
            color = "#873e23" if (i+j)%2==0 else "#eab676"
            C2.create_rectangle(x1,y1,x2,y2,fill=color,outline=color)
    # vẽ hậu & mobility
    for row, col in enumerate(state):
        x1 = size*col+offset
        y1 = size*row
        x2,y2 = x1+size, y1+size
        try:
            C2.create_image((x1+x2)/2,(y1+y2)/2,image=queen_img)
        except:
            C2.create_text((x1+x2)/2,(y1+y2)/2,text='Q',font=("Arial",24,"bold"))
        mob = mobility_of_queen(state,row,col)
        C2.create_text(x1+8,y1+10,text=str(mob),anchor="nw",
                       font=("Arial",10,"bold"),fill="white")
    # chỉ hiện cost khi UCS
    if current_algo == "UCS":
        tstate = tuple(state)
        cost = cost_map.get(tstate, cost_of_state(state))
        C2.create_text(250,560,text=f"Cost: {cost}",
                       font=("Arial",14,"bold"),fill="blue")
        cost_label.config(text=f"Cost: {cost}")
    else:
        cost_label.config(text="")

# ======================
# Auto-run
# ======================
def show_next_state():
    global current_index
    if current_index < len(current_path):
        draw_state(current_path[current_index])
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
        root.after(500, run_next_state)

def run_dfs_auto():
    global current_path, current_index, is_running, current_algo
    solutions = dfs_queens(N)
    if solutions:
        current_algo = "DFS"
        current_path = solutions[0]
        current_index = 0
        is_running = True
        run_next_state()

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
Button(btn_frame,text="⏯ Resume",font=("Arial",14,"bold"),
       bg="#4CAF50",fg="white",command=resume_run).grid(row=0,column=3,padx=10,pady=10)
Button(btn_frame,text="⏸ Stop",font=("Arial",14,"bold"),
       bg="#F44336",fg="white",command=stop_run).grid(row=0,column=4,padx=10,pady=10)
Button(btn_frame,text="🧹 Clear",font=("Arial",14,"bold"),
       bg="#9E9E9E",fg="white",command=clear_queens).grid(row=0,column=5,padx=10,pady=10)

for i in range(6):
    btn_frame.grid_columnconfigure(i, weight=1)

cost_label = Label(root, text="", font=("Arial",14), fg="blue")
cost_label.pack(pady=5)

# ======================
# Main loop
# ======================
root.mainloop()
