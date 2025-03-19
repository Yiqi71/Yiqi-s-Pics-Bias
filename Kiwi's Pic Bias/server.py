from flask import Flask, request, jsonify
import cv2
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# 加载评分模型
model = tf.keras.models.load_model('score_model.h5')

def process_uploaded_image(file):
    # 将文件转换为 OpenCV 格式
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    img = cv2.resize(img, (256, 256))  # 调整图片大小
    img = img / 255.0  # 归一化
    img = np.expand_dims(img, axis=0)  # 增加批次维度
    return img

@app.route('/compare', methods=['POST'])
def compare():
    if 'img1' not in request.files or 'img2' not in request.files:
        return jsonify({"error": "Please upload two images"}), 400

    # 读取上传的文件
    img1_file = request.files['img1']
    img2_file = request.files['img2']

    # 处理图像
    img1 = process_uploaded_image(img1_file)
    img2 = process_uploaded_image(img2_file)

    # 获取模型预测评分
    score1 = model.predict(img1)[0][0]
    score2 = model.predict(img2)[0][0]

    result = "You prefer the first image." if score1 > score2 else "You prefer the second image."

    return jsonify({
        "score1": score1,
        "score2": score2,
        "result": result
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # 启动 Flask 服务并指定端口
