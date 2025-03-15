import os
import random
import pandas as pd
from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime

folder_path = r"E:\纽大\Useless Machines\Yiqi's Pics Bias\animal_pics"
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]

# 加载评分
if os.path.exists('photo_scores.csv'):
    df = pd.read_csv('photo_scores.csv')
    elo_scores = {row['Photo']: row['Score'] for _, row in df.iterrows()}
else:
    df = pd.DataFrame(columns=["Photo", "Score", "Timestamp"])
    elo_scores = {file: 1000 for file in image_files}

for image in image_files:
    if image not in elo_scores:
        elo_scores[image] = 1000

def save_all_scores():
    score_df = pd.DataFrame([
        {"Photo": photo, "Score": score}
        for photo, score in elo_scores.items()
    ])
    score_df.to_csv('elo_scores.csv', index=False)

def update_elo(winner, loser, K=30):
    winner_score = elo_scores[winner]
    loser_score = elo_scores[loser]
    expected_winner = 1 / (1 + 10 ** ((loser_score - winner_score) / 400))
    expected_loser = 1 / (1 + 10 ** ((winner_score - loser_score) / 400))
    
    elo_scores[winner] += K * (1 - expected_winner)
    elo_scores[loser] += K * (0 - expected_loser)

def save_score(photo, score):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df.loc[len(df)] = [photo, score, timestamp]
    df.to_csv('photo_scores.csv', index=False)

MAX_SIZE = (600, 600)  # 最大显示尺寸

def resize_image(img):
    """将图片按比例缩放，最大尺寸为 600x600"""
    img_ratio = img.width / img.height
    max_width, max_height = MAX_SIZE

    # 计算新的尺寸，保持比例
    if img.width > img.height:
        new_width = max_width
        new_height = int(new_width / img_ratio)
    else:
        new_height =  max_height
        new_width = int(new_height * img_ratio)

    return img.resize((new_width, new_height), Image.LANCZOS)


def show_next_comparison():
    global photo_a, photo_b, photo_img_a, photo_img_b
    photo_a, photo_b = random.sample(image_files, 2)
    
    img_a = Image.open(os.path.join(folder_path, photo_a))
    img_b = Image.open(os.path.join(folder_path, photo_b))

    # 按比例缩放
    img_a = resize_image(img_a)
    img_b = resize_image(img_b)
    
    photo_img_a = ImageTk.PhotoImage(img_a)
    photo_img_b = ImageTk.PhotoImage(img_b)

    label_a.config(image=photo_img_a)
    label_a.image = photo_img_a
    label_b.config(image=photo_img_b)
    label_b.image = photo_img_b

def choose_winner(winner):
    loser = photo_b if winner == photo_a else photo_a
    update_elo(winner, loser)
    save_score(winner, elo_scores[winner])
    save_score(loser, elo_scores[loser])
    save_all_scores()  # 自动保存 Elo 分数
    show_next_comparison()


# GUI
root = tk.Tk()
root.title("Photo Comparison")

frame = tk.Frame(root)
frame.pack()

label_a = tk.Label(frame)
label_a.grid(row=0, column=0, padx=10, pady=10)

label_b = tk.Label(frame)
label_b.grid(row=0, column=1, padx=10, pady=10)

button_a = tk.Button(frame, text="Choose Left", command=lambda: choose_winner(photo_a))
button_a.grid(row=1, column=0, pady=10)

button_b = tk.Button(frame, text="Choose Right", command=lambda: choose_winner(photo_b))
button_b.grid(row=1, column=1, pady=10)

show_next_comparison()
root.mainloop()
