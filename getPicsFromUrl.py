import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 配置 Selenium，使用 Chrome 浏览器
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 无头模式，不显示浏览器窗口
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 设置保存图片的文件夹路径
folder_path = r"E:\纽大\Useless Machines\Yiqi's Pics Bias\dog_pics"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 要爬取的网页URL
url = "https://unsplash.com/s/photos/dog"
try:
    # 访问 Google 图片搜索页面
    driver.get(url)
    time.sleep(2)  # 等待页面加载

    # 模拟滚动加载多次，确保更多图片加载
    for _ in range(5):  
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # 获取页面 HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # 找到所有图片的URL
    img_tags = soup.find_all("img")
    img_urls = [img["src"] for img in img_tags if img.get("src") and not img["src"].startswith("data:")]

    # 只下载前 800 张
    max_images = 200
    img_urls = img_urls[:max_images]

    print(f"找到 {len(img_urls)} 张图片")

    # 遍历图片链接，下载并保存到本地
    for idx, img_url in enumerate(img_urls, 1):
        try:
            # 获取图片内容
            img_response = requests.get(img_url, timeout=5)

            # 设置图片保存的文件名
            img_name = f"unsplash-dog-{idx}.jpg"
            img_path = os.path.join(folder_path, img_name)

            # 保存图片
            with open(img_path, "wb") as f:
                f.write(img_response.content)

            print(f"图片 {img_name} 已下载并保存到 {img_path}")

        except Exception as e:
            print(f"下载图片失败: {img_url}, 错误: {e}")

finally:
    # 关闭 Selenium
    driver.quit()
