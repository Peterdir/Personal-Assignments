from tkinter import *
import os
from PIL import Image, ImageTk

root = Tk()
root.geometry("1300x725+10+10")
root.title("Cờ vua Việt")


C1 = Canvas(root, bg="white",
           height=500, width=500)
C1.place(x = 50, y = 30)

C2 = Canvas(root, bg="white",
            height=500, width=500)
C2.place(x=650, y=30)

size = 62.5
N = 8

def table_initial():
    for i in range(N):
        for j in range(N):
            x1 = size * i
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
            x1 = size * i
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

# Button
btn_shuffle = Button(root,
                     text="Shuffle",
                     height=5,
                     width=10)
btn_shuffle.place(x=0, y =600)

btn_solve = Button(root,
                     text="Shuffle",
                     height=5,
                     width=10)
root.mainloop()
