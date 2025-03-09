import os
import random
import pandas as pd
from PIL import Image
from datetime import datetime

# 获取文件夹中所有图片的路径
folder_path = r"E:\纽大\Useless Machines\Yiqi's Pics Bias\animal_pics"
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]


# 加载之前的评分记录
if os.path.exists('photo_scores.csv'):
    df = pd.read_csv('photo_scores.csv')
    # 恢复 Elo 评分（基于保存的数据）
    elo_scores = {row['Photo']: row['Score'] for _, row in df.iterrows()}
else:
    # 如果没有记录文件，就初始化一个新的数据框
    df = pd.DataFrame(columns=["Photo", "Score", "Timestamp"])
    elo_scores = {file: 1000 for file in image_files}  # 初始评分为 1000

# 对比时如果是新图片，初始化 Elo 评分为 1000
for image in image_files:
    if image not in elo_scores:
        elo_scores[image] = 1000

def show_image(image_path):
    img = Image.open(image_path)
    img.show()

def update_elo(winner, loser, K=30):
    # 更新Elo评分
    winner_score = elo_scores[winner]
    loser_score = elo_scores[loser]
    expected_winner = 1 / (1 + 10 ** ((loser_score - winner_score) / 400))
    expected_loser = 1 / (1 + 10 ** ((winner_score - loser_score) / 400))
    
    elo_scores[winner] += K * (1 - expected_winner)
    elo_scores[loser] += K * (0 - expected_loser)

def save_score(photo, score):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df.loc[len(df)] = [photo, score, timestamp]
    df.to_csv('photo_scores.csv', index=False)  # 保存到文件

# 执行对比并打分
def compare_photos():
    while len(image_files) > 1:
        # 随机选择两张照片进行对比
        photo_a, photo_b = random.sample(image_files, 2)
        show_image(os.path.join(folder_path, photo_a))
        # input(f"Press Enter when you finish viewing {photo_a}.")
        show_image(os.path.join(folder_path, photo_b))
        # input(f"Press Enter when you finish viewing {photo_b}.")
        
        # 记录你的选择（你可以自己手动输入，或者按某个规则决定）
        winner = input(f"Which photo do you prefer? (Enter 'a' for {photo_a}, 'b' for {photo_b}): ")
        if winner == 'a':
            update_elo(photo_a, photo_b)
            save_score(photo_a, elo_scores[photo_a])
            save_score(photo_b, elo_scores[photo_b])
        elif winner == 'b':
            update_elo(photo_b, photo_a)
            save_score(photo_a, elo_scores[photo_a])
            save_score(photo_b, elo_scores[photo_b])
        else:
            print("Invalid input. Please try again.")
            continue

# 启动比较任务
compare_photos()

# cmd
# cd /d E:\纽大\Useless Machines\Yiqi's Pics Bias