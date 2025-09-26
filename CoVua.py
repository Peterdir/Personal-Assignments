# N-Queens GUI with BFS/DFS/UCS (mobility-based cost, cost chỉ hiện khi UCS)
# ======================
# Import
# ======================
from queue import Queue, PriorityQueue
from tkinter import *
import os
import math
import numpy as np
from Algorithm import *
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
step_delay = 10
dfs_gen = None 
bfs_gen = None
ucs_gen = None
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
    draw_labels(C1)
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
                if tuple(new_state) not in parent:
                    parent[tuple(new_state)] = (state)
                    stack.append(new_state)
                    yield ("push", new_state)  # báo là thêm trạng thái mới vào stack

def bfs_generator(N):
    q = Queue()
    q.put([])
    parent = {tuple([]): None}
    while not q.empty():
        state = q.get()
        yield ("visit", state)
        if len(state) == N:
            yield ("found", tuple(state), parent)
            return
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                if tuple(new_state) not in parent:
                    parent[tuple(new_state)] = (state)
                    q.put(new_state)
                    yield ("push", new_state)

def ucs_generator(N):
    pq = PriorityQueue()
    pq.put((0, []))

    parent = {tuple([]): None}
    cost_map = {tuple([]): 0}

    while not pq.empty():
        cost, state = pq.get()
        yield ("visit", state, cost)
        if len(state) == N:
            yield ("found", state, parent, cost_map)
            return
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                new_cost = cost_of_state(new_state)
                t_new_state = tuple(new_state)
                if t_new_state not in cost_map or new_cost < cost_map[t_new_state]:
                    parent[t_new_state] = tuple(state)
                    cost_map[t_new_state] = new_cost
                    pq.put((new_cost, new_state))
                    yield ("push", new_state, new_cost)


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
after_id = None
def reset_before_run():
    global is_running, current_path, current_index, current_algo, after_id
    is_running = False
    current_path = []
    current_index = 0
    current_algo = None

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

def show_next_state():
    global current_index
    if current_index < len(current_path):
        draw_state_on_canvas(C1, current_path[current_index], show_mobility=True, show_cost=None)
        current_index += 1

def resume_run():
    global is_running
    is_running = True

    if current_algo == "DFS":
        try:
            run_dfs_step()
        except NameError:
            pass
    elif current_algo == "BFS":
        try:
            run_bfs_step()
        except NameError:
            pass
    else:
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
    reset_before_run()
    global dfs_gen, current_algo, is_running
    solutions = dfs_queens(N)
    if solutions:
        final_solution = solutions[0][-1] 
        draw_state_on_canvas(C2, final_solution, show_mobility=False)
    
    dfs_gen = dfs_generator(N)
    current_algo = "DFS"
    is_running = True
    run_dfs_step()

def run_bfs_auto():
    reset_before_run()
    global bfs_gen, current_algo, is_running
    solutions = bfs_queens(N)
    if solutions:
        final_solution = solutions[0][-1]
        draw_state_on_canvas(C2, final_solution, show_mobility=False)
    bfs_gen = bfs_generator(N)
    current_algo = "BFS"
    is_running = True
    run_bfs_step()

def run_ucs_auto():
    reset_before_run()
    global ucs_gen, current_algo, is_running
    ucs_gen = ucs_generator(N)
    current_algo = "UCS"
    is_running = True
    run_ucs_step()

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

def run_hill_auto():
    global current_path, current_index, is_running, current_algo
    solution, h_val = hillClimbing_search()
    if solution is not None:
        current_algo = "Hill Climbing"
        
        current_path = [solution]
        current_index = 0
        is_running = True
        run_next_state()

def run_simulatedAnealling_auto():
    global current_path, current_index, is_running, current_algo
    solution, h_val = simulated_annealing()
    if solution is not None:
        current_algo = "Simulated Annealing"
        
        current_path = [solution]
        current_index = 0
        is_running = True
        run_next_state()

def run_localBeam_auto():
    global current_path, current_index, is_running, current_algo
    solution, h_val = local_beam_search()
    if solution is not None:
        current_algo = "Local Beam"
        
        current_path = [solution]
        current_index = 0
        is_running = True
        run_next_state()

def run_Genetic_auto():
    global current_path, current_index, is_running, current_algo
    solution, h_val = genetic_algorithm()
    if solution is not None:
        current_algo = "Genetic algorithm"
        
        current_path = [solution]
        current_index = 0
        is_running = True
        run_next_state()

# ======================
# Step-by-step
# ======================
def run_dfs_step():
    global dfs_gen, is_running, after_id
    if not is_running:
        return
    try:
        event = next(dfs_gen)
        if event[0] in ("visit", "push"):
            state = event[1]
            draw_state_on_canvas(C1, state, show_mobility=False)
        elif event[0] == "found":
            final_state = list(event[1])
            draw_state_on_canvas(C2, final_state, show_mobility=False)
            is_running = False
            return
        after_id = root.after(step_delay, run_dfs_step)
    except StopIteration:
        is_running = False

def run_bfs_step():
    global bfs_gen, is_running, after_id
    if not is_running:
        return
    try:
        event = next(bfs_gen)
        if event[0] in ("visit", "push"):
            state = event[1]
            draw_state_on_canvas(C1, state, show_mobility=False)
        elif event[0] == "found":
            final_state = list(event[1])
            draw_state_on_canvas(C2, final_state, show_mobility=False)
            is_running = False
            return
        after_id = root.after(step_delay, run_bfs_step)
    except StopIteration:
        is_running = False

def run_ucs_step():
    global ucs_gen, is_running, after_id
    if not is_running:
        return
    try:
        event = next(ucs_gen)
        if event[0] in ("visit", "push"):
            state, cost = event[1], event[2]
            draw_state_on_canvas(C1, state, show_mobility=True, show_cost=cost)
        elif event[0] == "found":
            final_state, cost_map = list(event[1]), event[3]
            draw_state_on_canvas(C2, final_state, show_mobility=True,
                                 show_cost=cost_map[tuple(final_state)])
            is_running = False
            return
        after_id = root.after(step_delay, run_ucs_step)
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
btn_frame.pack(side=BOTTOM, pady=10, fill="x")

# Hàng 1: classical search
Button(btn_frame, text="🌐 BFS", font=("Arial",14,"bold"),
       bg="#009688", fg="white", width=18,
       command=run_bfs_auto).grid(row=0, column=0, padx=5, pady=5)
Button(btn_frame, text="🌲 DFS", font=("Arial",14,"bold"),
       bg="#795548", fg="white", width=18,
       command=run_dfs_auto).grid(row=0, column=1, padx=5, pady=5)
Button(btn_frame, text="💰 UCS", font=("Arial",14,"bold"),
       bg="#3F51B5", fg="white", width=18,
       command=run_ucs_auto).grid(row=0, column=2, padx=5, pady=5)
Button(btn_frame, text="DLS", font=("Arial",14,"bold"),
       bg="#9E9E9E", fg="white", width=18,
       command=run_dls_auto).grid(row=0, column=3, padx=5, pady=5)
Button(btn_frame, text="IDS", font=("Arial",14,"bold"),
       bg="#9E9E9E", fg="white", width=18,
       command=run_ids_auto).grid(row=0, column=4, padx=5, pady=5)

# Hàng 2: heuristic search
Button(btn_frame, text="Greedy Best-First", font=("Arial",14,"bold"),
       bg="#9E9E9E", fg="white", width=18,
       command=run_gbfs_auto).grid(row=1, column=0, padx=5, pady=5)
Button(btn_frame, text="A* Search", font=("Arial",14,"bold"),
       bg="#FF9800", fg="white", width=18,
       command=run_astar_auto).grid(row=1, column=1, padx=5, pady=5)
Button(btn_frame, text="Hill Climbing", font=("Arial",14,"bold"),
       bg="#607D8B", fg="white", width=18,
       command=run_hill_auto).grid(row=1, column=2, padx=5, pady=5)
Button(btn_frame, text="Simulated Annealing", font=("Arial",14,"bold"),
       bg="#607D8B", fg="white", width=18,
       command=run_simulatedAnealling_auto).grid(row=1, column=3, padx=5, pady=5)

# Hàng 3: beam, GA, control
Button(btn_frame, text="Local Beam", font=("Arial",14,"bold"),
       bg="#607D8B", fg="white", width=18,
       command=run_localBeam_auto).grid(row=2, column=0, padx=5, pady=5)
Button(btn_frame, text="Genetic Algorithm", font=("Arial",14,"bold"),
       bg="#607D8B", fg="white", width=18,
       command=run_Genetic_auto).grid(row=2, column=1, padx=5, pady=5)
Button(btn_frame, text="⏯ Resume", font=("Arial",14,"bold"),
       bg="#4CAF50", fg="white", width=18,
       command=resume_run).grid(row=2, column=2, padx=5, pady=5)
Button(btn_frame, text="⏸ Stop", font=("Arial",14,"bold"),
       bg="#F44336", fg="white", width=18,
       command=stop_run).grid(row=2, column=3, padx=5, pady=5)
Button(btn_frame, text="🧹 Clear", font=("Arial",14,"bold"),
       bg="#9E9E9E", fg="white", width=18,
       command=clear_queens).grid(row=2, column=4, padx=5, pady=5)

# Căn đều các cột
for i in range(5):
    btn_frame.grid_columnconfigure(i, weight=1)


cost_label = Label(root, text="", font=("Arial",14), fg="blue")
cost_label.pack(pady=5)

# ======================
# Main loop
# ======================
root.mainloop()
