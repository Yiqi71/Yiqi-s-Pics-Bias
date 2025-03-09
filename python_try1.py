import os
import csv
from PIL import Image

# 设置图片文件夹路径
folder_path = r"E:\纽大\Useless Machines\Yiqi's Pics Bias\pictures"

# 获取所有图片文件
pictures = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# 创建CSV文件并写入表头
with open("picture_scores_try1.csv", "w", newline="") as csvfile:
    fieldnames = ["pic_src", "familiarity", "people_with", "position", "activity", "my_reaction", "my_score"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # 遍历所有图片并询问评分和信息
    for pic_name in pictures:
        pic_path = os.path.join(folder_path, pic_name)

        # 展示图片
        image = Image.open(pic_path)
        image.show()  # 这会弹出图片查看器来显示图片

        # 获取用户输入的信息
        print(f"请输入图片 {pic_name} 的信息:")
        familiarity = input("familiarity(0-10): ")
        people_with = input("people_with: ")
        position = input("position: ")
        activity = input("activity: ")
        my_reaction = input("my_reaction: ")
        try:
            my_score = float(input("score (0-10): "))
        except ValueError:
            my_score = 5.0
        
        # 关闭图片查看器（有些系统上需要）
        image.close()

        # 写入CSV文件
        writer.writerow({
            "pic_src": pic_path,
            "familiarity": familiarity,
            "people_with": people_with,
            "position": position,
            "activity": activity,
            "my_reaction": my_reaction,
            "my_score": my_score
        })

        print(f"图片 {pic_name} 的数据已保存。\n")
