import os
import random
import pandas as pd
from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime

folder_path = r"E:\\纽大\\Useless Machines\\Yiqi's Pics Bias\\dog_pics"
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]

# 加载评分
df_scores_path = 'dog_photo_scores.csv'
df_elo_path = 'dog_elo_scores.csv'

if os.path.exists(df_scores_path):
    df = pd.read_csv(df_scores_path)
    df = df[df['Photo'].isin(image_files)]  # 删除已不存在的图片记录
    df.to_csv(df_scores_path, index=False)
    elo_scores = {row['Photo']: row['Score'] for _, row in df.iterrows()}
else:
    df = pd.DataFrame(columns=["Photo", "Score", "Timestamp"])
    elo_scores = {file: 1000 for file in image_files}

if os.path.exists(df_elo_path):
    df_elo = pd.read_csv(df_elo_path)
    df_elo = df_elo[df_elo['Photo'].isin(image_files)]  # 删除已不存在的图片记录
    df_elo.to_csv(df_elo_path, index=False)

elo_scores = {photo: elo_scores.get(photo, 1000) for photo in image_files}

def save_all_scores():
    score_df = pd.DataFrame([
        {"Photo": photo, "Score": score}
        for photo, score in elo_scores.items()
    ])
    score_df.to_csv('dog_elo_scores.csv', index=False)

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
    df.to_csv('dog_photo_scores.csv', index=False)

MAX_SIZE = (600, 600)

def resize_image(img):
    img_ratio = img.width / img.height
    max_width, max_height = MAX_SIZE

    if img.width > img.height:
        new_width = max_width
        new_height = int(new_width / img_ratio)
    else:
        new_height = max_height
        new_width = int(new_height * img_ratio)

    return img.resize((new_width, new_height), Image.LANCZOS)
def show_next_comparison():
    global photo_a, photo_b, photo_img_a, photo_img_b

    # 先移动 result_label 到新的图片下面
    result_label.grid(row=2, column=0, columnspan=2, pady=10)  

    # 选取两张新图片
    photo_a, photo_b = random.sample(image_files, 2)

    img_a = Image.open(os.path.join(folder_path, photo_a))
    img_b = Image.open(os.path.join(folder_path, photo_b))

    img_a = resize_image(img_a)
    img_b = resize_image(img_b)

    photo_img_a = ImageTk.PhotoImage(img_a)
    photo_img_b = ImageTk.PhotoImage(img_b)

    label_a.config(image=photo_img_a)
    label_a.image = photo_img_a
    label_b.config(image=photo_img_b)
    label_b.image = photo_img_b

    # 显示文件名
    score_label_a.config(text=photo_a)
    score_label_b.config(text=photo_b)

def choose_winner(winner):
    loser = photo_b if winner == photo_a else photo_a

    # 判断选择是否与 Elo 分数一致
    correct_choice = elo_scores[winner] > elo_scores[loser]
    
    # 只有在选择错误时才显示 "false"
    if correct_choice:
        result_label.config(text="")  # 选择正确，清空文本
    else:
        result_label.config(text="false", fg="red")  # 选择错误，显示 "false"（红色）

    update_elo(winner, loser)
    save_score(winner, elo_scores[winner])
    save_score(loser, elo_scores[loser])
    save_all_scores()
    show_next_comparison()


def key_pressed(event):
    if event.char in ('a', 'j'):
        choose_winner(photo_a)
    elif event.char in ('d', 'l'):
        choose_winner(photo_b)

# GUI
root = tk.Tk()
root.title("Photo Comparison")
root.bind('<Key>', key_pressed)

frame = tk.Frame(root)
frame.pack(pady=20)

label_a = tk.Label(frame)
label_a.grid(row=0, column=0, padx=20, pady=10)

label_b = tk.Label(frame)
label_b.grid(row=0, column=1, padx=20, pady=10)

# 显示文件名的栏
score_label_a = tk.Label(frame, text="", font=("Arial", 12))
score_label_a.grid(row=1, column=0, pady=5)

score_label_b = tk.Label(frame, text="", font=("Arial", 12))
score_label_b.grid(row=1, column=1, pady=5)

# 这里才初始化 result_label，放在 frame 里，并且跨两列
result_label = tk.Label(frame, text="", font=("Arial", 14), fg="black")
result_label.grid(row=2, column=0, columnspan=2, pady=10)  # 跨两列，放在文件名下面

show_next_comparison()
root.mainloop()
