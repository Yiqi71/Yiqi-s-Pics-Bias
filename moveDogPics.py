import pandas as pd
import shutil
import os

# 读取CSV文件
csv_file = 'dogs_manual_score.csv'
df = pd.read_csv(csv_file)

# 设置图片文件夹路径
image_folder = 'dog_likeOrNot'
like_folder = 'dog_likeOrNot/like'
soso_folder = 'dog_likeOrNot/soso'
dont_like_folder = 'dog_likeOrNot/dont_like'

# 创建目标文件夹（如果不存在的话）
os.makedirs(like_folder, exist_ok=True)
os.makedirs(soso_folder, exist_ok=True)
os.makedirs(dont_like_folder, exist_ok=True)

# 遍历每一行并移动文件
for index, row in df.iterrows():
    image_file = row['Photo']  # 确保你的CSV列名是'filename'
    score = row['Score']  # 确保你的CSV列名是'score'
    
    # 拼接完整路径
    image_path = os.path.join(image_folder, image_file)
    
    # 判断评分，决定移动到哪个文件夹
    if score > 1000:
        destination = like_folder
    elif score > 950:
        destination = soso_folder
    else:
        destination = dont_like_folder
    
    # 移动文件
    shutil.move(image_path, os.path.join(destination, image_file))

print("文件已成功移动。")
