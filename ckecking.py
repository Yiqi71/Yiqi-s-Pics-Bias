import os
import pandas as pd
import tkinter as tk
from tkinter import Label, Button, Entry
from PIL import Image, ImageTk

# 读取 CSV 文件
df = pd.read_csv("dog_elo_scores.csv")

dog_images = df["Photo"].tolist()
dog_scores = df["Score"].tolist()

img_dir = "dog_pics"
current_index = 0

def update_image():
    global current_index, img_label, score_entry
    
    img_path = os.path.join(img_dir, dog_images[current_index])
    img = Image.open(img_path)
    img = img.resize((300, 300))
    img_tk = ImageTk.PhotoImage(img)
    
    img_label.config(image=img_tk)
    img_label.image = img_tk
    
    score_entry.delete(0, tk.END)
    score_entry.insert(0, str(dog_scores[current_index]))
    
    window.title(f"Image {current_index + 1} of {len(dog_images)}")

def save_score():
    global current_index
    new_score = score_entry.get()
    
    try:
        dog_scores[current_index] = float(new_score)
        df.at[current_index, "Score"] = float(new_score)
        df.to_csv("dog_elo_scores.csv", index=False)
    except ValueError:
        print("Invalid score input")

def next_image():
    global current_index
    if current_index < len(dog_images) - 1:
        save_score()
        current_index += 1
        update_image()

def prev_image():
    global current_index
    if current_index > 0:
        save_score()
        current_index -= 1
        update_image()

# 创建 GUI 界面
window = tk.Tk()
window.title("Dog Image Score Checker")

img_label = Label(window)
img_label.pack()

score_entry = Entry(window, font=("Arial", 14))
score_entry.pack()

prev_button = Button(window, text="Previous", command=prev_image)
prev_button.pack(side=tk.LEFT)

next_button = Button(window, text="Next", command=next_image)
next_button.pack(side=tk.RIGHT)

update_image()

window.mainloop()
