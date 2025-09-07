import backtrackingSolution
from queue import Queue
from tkinter import *
import os
from PIL import Image, ImageTk

root = Tk()
root.geometry("1300x725+10+10")
root.title("Cờ vua Việt")


C1 = Canvas(root, bg="white",
           height=540, width=540)
C1.place(x=50, y=30)

C2 = Canvas(root, bg="white",
            height=540, width=540)
C2.place(x=650, y=30)

size = 62.5
N = 8
offset = 30
size_col = 10

def draw_labels(canvas):
    cols = ['1', '2', '3', '4', '5', '6', '7', '8']
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    for i in range(N):
        y = size * i + size/2
        canvas.create_text(size_col, y, text=cols[i], font=("Arial", 12, "bold"))

    for i in range(N):
        x = size * i + offset + size/2
        canvas.create_text(x, N * size + 15, text=rows[i], font=("Arial", 12, "bold"))

def table_initial():
    for i in range(N):
        for j in range(N):
            x1 = size * i + offset 
            y1 = size * j
            x2 = x1 + size
            y2 = y1 + size
            if (i + j) % 2 == 0:
                rectangle = C1.create_rectangle(x1, y1, x2, y2, fill="#873e23")
            else:
                rectangle = C1.create_rectangle(x1, y1, x2, y2, fill="#eab676")

queens = [['1', '0', '0', '0', '0', '0', '0', '0'],
          ['0', '0', '1', '0', '0', '0', '0', '0'],
          ['0', '1', '0', '0', '0', '0', '0', '0'],
          ['0', '0', '0', '1', '0', '0', '0', '0'],
          ['0', '0', '0', '0', '0', '1', '0', '0'],
          ['0', '0', '0', '0', '0', '0', '0', '1'],
          ['0', '0', '0', '0', '1', '0', '0', '0'],
          ['0', '0', '0', '0', '0', '0', '1', '0']]


# Tạo hàm sinh trạng thái
def check_queens(state, col):
    row = len(state)
    for r in range(row):
        c = state[r]
        if c == col:
            return False
        if abs(r - row) == abs(c - col):
            return False
    
    return True

def bfs_queens(N):
    q = Queue()
    start = []
    q.put(start)
    parent = {tuple(start): None}
    solutions = []

    while not q.empty():
        state = q.get()

        if len(state) == N:
            path = []
            s = tuple(state)
            while s is not None: 
                path.append(list(s))
                s = parent[s]
            path.reverse()
            solutions.append(path)
            continue
        
        for col in range(N):
            if check_queens(state, col):
                new_state = state + [col]
                if tuple(new_state) not in parent:
                    parent[tuple(new_state)] = tuple(state)
                    q.put(new_state)

    return solutions

current_path = []
current_index = 0

def draw_state(state):
    C2.delete("all")  # xoá bàn cũ
    # vẽ bàn cờ lại
    draw_labels(C2)
    for i in range(N):
        for j in range(N):
            x1 = size * i + offset
            y1 = size * j
            x2 = x1 + size
            y2 = y1 + size
            color = "#873e23" if (i+j) % 2 == 0 else "#eab676"
            C2.create_rectangle(x1, y1, x2, y2, fill=color)
    # vẽ các quân hậu trong state
    for row, col in enumerate(state):
        x1 = size * row + offset
        y1 = size * col
        x2 = x1 + size
        y2 = y1 + size
        C2.create_image((x1 + x2) / 2, (y1 + y2) / 2, image=queen_img)

def prepare_bfs_solution():
    global current_path, current_index
    solutions = bfs_queens(N)
    if len(solutions) > 0:
        current_path = solutions[0]   # lấy đường đi của lời giải đầu tiên
        current_index = 0
    else:
        current_path = []
        current_index = 0

def show_next_state():
    global current_index
    if current_index < len(current_path):
        draw_state(current_path[current_index])
        current_index += 1


current_path = os.path.dirname(os.path.abspath(__file__))
queen_path = os.path.join(current_path, "wq.png")
img = Image.open(queen_path)
img = img.resize((int(size), int(size)), Image.Resampling.LANCZOS)
queen_img = ImageTk.PhotoImage(img)

def table_operator():
    queensTest = [-1] * 8
    backtrackingSolution.solve(0, queensTest)
    for i in range(N):
        for j in range(N):
            x1 = size * i + offset
            y1 = size * j
            x2 = x1 + size
            y2 = y1 + size
            if (i + j) % 2 == 0:
                rectangle = C2.create_rectangle(x1, y1, x2, y2, fill="#873e23")
            else:
                rectangle = C2.create_rectangle(x1, y1, x2, y2, fill="#eab676")
            # if queens[i][j] == '1':
            #     C2.create_image((x1 + x2)/2, (y1 + y2)/2,
            #                     image=queen_img)
    #         if len(backtrackingSolution.Solutions) > 0:
    #             result = backtrackingSolution.Solutions[0]

    # if len(backtrackingSolution.Solutions) > 0:
    #     result = backtrackingSolution.Solutions[0]
    #     for row in range(len(result)):
    #         x1 = size * row + offset
    #         y1 = size * result[row]
    #         x2 = x1 + size
    #         y2 = y1 + size
    #         C2.create_image((x1 + x2)/2, (y1 + y2)/2,
    #                         image=queen_img)
                

table_initial()
table_operator()
draw_labels(C1)
draw_labels(C2)

# Button

btn_frame = Frame(root, bg="white")
btn_frame.place(x=500, y=600)

# Shuffle
btn_shuffle = Button(btn_frame,
                     text="Shuffle",
                     font=("Arial", 14, "bold"),
                     bg="#4CAF50", fg="white",
                     activebackground="#45a049",
                     relief="raised", bd=3,
                     padx=20, pady=10)
btn_shuffle.grid(row=0, column=0, padx=20)

# BFS solve
btn_prepare = Button(btn_frame,
                     text="🔍 BFS Solve",
                     font=("Arial", 14, "bold"),
                     bg="#9C27B0", fg="white",
                     command=prepare_bfs_solution)
btn_prepare.grid(row=0, column=3, padx=20)

# BFS generate state
btn_next = Button(btn_frame,
                  text="➡ Next",
                  font=("Arial", 14, "bold"),
                  bg="#FF9800", fg="white",
                  command=show_next_state)
btn_next.grid(row=0, column=2, padx=20)

# btn_solve = Button(btn_frame,
#                    text="🤖 Solve",
#                    font=("Arial", 14, "bold"),
#                    bg="#2196F3", fg="white",
#                    activebackground="#0b7dda",
#                    relief="raised", bd=3,
#                    padx=20, pady=10)
# btn_solve.grid(row=0, column=1, padx=20)

root.mainloop()
