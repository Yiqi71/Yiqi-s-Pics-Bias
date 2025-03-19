import os
import pandas as pd
import tkinter as tk
from tkinter import Label, Button, Entry, Frame
from PIL import Image, ImageTk

# 读取 CSV 文件
df = pd.read_csv("dogs_manual_score.csv")

# 将图片文件名和分数列放入列表中
dog_images = df["Photo"].tolist()
dog_scores = df["Score"].tolist()

# 将图片和分数打包成元组并进行排序，确保图片和分数的对应关系不变
sorted_images_scores = sorted(zip(dog_images, dog_scores), key=lambda x: x[1])

# 解包回两个列表
dog_images, dog_scores = zip(*sorted_images_scores)

# 转换为列表
dog_images = list(dog_images)
dog_scores = list(dog_scores)

img_dir = "dog_pics"
current_index = 0

def update_images():
    global current_index, img_labels, score_entries
    
    # 更新图片和输入框，显示 10 张图片
    for i in range(10):
        img_idx = current_index + i
        if img_idx < len(dog_images):
            img_path = os.path.join(img_dir, dog_images[img_idx])
            img = Image.open(img_path)
            
            # 按原比例调整图片大小，宽度设置为 250，高度根据比例计算
            img_width = 250
            img_height = int(img.height * (img_width / img.width))
            img = img.resize((img_width, img_height))
            
            img_tk = ImageTk.PhotoImage(img)
            
            # 更新图片
            img_labels[i].config(image=img_tk)
            img_labels[i].image = img_tk

            # 更新分数输入框
            score_entries[i].delete(0, tk.END)
            score_entries[i].insert(0, str(dog_scores[img_idx]))
    
    window.title(f"Image {current_index + 1} to {min(current_index + 10, len(dog_images))} of {len(dog_images)}")

def save_scores():
    global current_index
    for i in range(10):
        img_idx = current_index + i
        if img_idx < len(dog_images):
            new_score = score_entries[i].get()
            try:
                dog_scores[img_idx] = float(new_score)
                df.at[img_idx, "Score"] = float(new_score)
            except ValueError:
                print(f"Invalid score input for image {dog_images[img_idx]}")
    
    # 保存数据到新的 CSV 文件
    df.to_csv("dogs_manual_score.csv", index=False)

def next_images():
    global current_index
    if current_index + 10 < len(dog_images):
        save_scores()
        current_index += 10  # 显示下一组 10 张图片
        update_images()

def prev_images():
    global current_index
    if current_index > 0:
        save_scores()
        current_index -= 10  # 返回上一组 10 张图片
        update_images()

# 创建 GUI 界面
window = tk.Tk()
window.title("Dog Image Score Checker")

# 创建框架，将图片分成两行：上面 5 张，下面 5 张
img_labels = []
score_entries = []
frame_top = Frame(window)
frame_top.pack()

frame_bottom = Frame(window)
frame_bottom.pack()

# 上面5张图片
for _ in range(5):
    img_frame = Frame(frame_top)
    img_frame.pack(side=tk.LEFT, padx=5, pady=5)
    
    img_label = Label(img_frame)
    img_label.pack()
    img_labels.append(img_label)

    score_entry = Entry(img_frame, font=("Arial", 14), width=5)
    score_entry.pack()
    score_entries.append(score_entry)

# 下面5张图片
for _ in range(5):
    img_frame = Frame(frame_bottom)
    img_frame.pack(side=tk.LEFT, padx=5, pady=5)
    
    img_label = Label(img_frame)
    img_label.pack()
    img_labels.append(img_label)

    score_entry = Entry(img_frame, font=("Arial", 14), width=5)
    score_entry.pack()
    score_entries.append(score_entry)

# 创建按钮
prev_button = Button(window, text="Previous", command=prev_images)
prev_button.pack(side=tk.LEFT)

next_button = Button(window, text="Next", command=next_images)
next_button.pack(side=tk.RIGHT)

update_images()

window.mainloop()
