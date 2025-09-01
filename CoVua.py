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

current_path = os.path.dirname(os.path.abspath(__file__))
queen_path = os.path.join(current_path, "wq.png")
img = Image.open(queen_path)
img = img.resize((int(size), int(size)), Image.Resampling.LANCZOS)
queen_img = ImageTk.PhotoImage(img)

def table_operator():
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
            if queens[i][j] == '1':
                C2.create_image((x1 + x2)/2, (y1 + y2)/2,
                                image=queen_img)
    





table_initial()
table_operator()
draw_labels(C1)
draw_labels(C2)

# Button

btn_frame = Frame(root, bg="white")
btn_frame.place(x=500, y=600)

btn_shuffle = Button(btn_frame,
                     text="Shuffle",
                     font=("Arial", 14, "bold"),
                     bg="#4CAF50", fg="white",
                     activebackground="#45a049",
                     relief="raised", bd=3,
                     padx=20, pady=10)
btn_shuffle.grid(row=0, column=0, padx=20)


btn_solve = Button(btn_frame,
                   text="🤖 Solve",
                   font=("Arial", 14, "bold"),
                   bg="#2196F3", fg="white",
                   activebackground="#0b7dda",
                   relief="raised", bd=3,
                   padx=20, pady=10)
btn_solve.grid(row=0, column=1, padx=20)

root.mainloop()
