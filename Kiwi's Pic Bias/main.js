let scoreA = 0;
let scoreB = 0;

function retryUpload() {
    document.getElementById("resultModal").style.display = "none";
    goToUploadPage(); // 回到上传页面
    filesUploaded = false;
    setTimeout(() => {
        const hand = document.querySelector('#handImage');
        hand.style.transition = "top 2s ease-in-out, opacity 1s";
        hand.style.top = "-150px"; // 移动到目标位置
        hand.style.opacity = "0"; // 显示
    }, 2000);
}

function closeModal() {
    document.getElementById("resultModal").style.display = "none"; // 关闭弹窗
}


// 生成0到5之间的随机分数
function generateRandomScores() {
    scoreA = Math.floor(Math.random() * 6); // 生成0到5之间的随机数
    scoreB = Math.floor(Math.random() * 6); // 生成0到5之间的随机数
}

// 从URL中获取传递的分数
function getScoresFromURL() {
    // 根据分数推荐照片
    const handImage = document.getElementById('handImage');
    const leftArea = document.getElementById('leftHandArea').getBoundingClientRect();
    const rightArea = document.getElementById('rightHandArea').getBoundingClientRect();

    // 计算 handImage 的新位置
    if (scoreA > scoreB) {
        handImage.style.left = `${leftArea.left + leftArea.width / 2}px`;
    } else {
        handImage.style.left = `${rightArea.left + rightArea.width / 2}px`;
    }

    document.getElementById("recommendation").style.opacity = 0;
}

// python server.py
async function compareImages() {
    const photoAInput = document.getElementById('photoAInput').files[0];
    const photoBInput = document.getElementById('photoBInput').files[0];

    // if (!photoAInput || !photoBInput) {
    //     alert("Please upload both images.");
    //     return;
    // }

    let formData = new FormData();
    formData.append("img1", photoAInput);
    formData.append("img2", photoBInput);

    try {
        let response = await fetch('http://127.0.0.1:5001/compare', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        let data = await response.json(); // 解析响应为JSON
        document.getElementById('result').innerText = data.result;

        let hand = document.getElementById('handImage');
        hand.style.left = data.score1 > data.score2 ? '30vw' : '60vw';
    } catch (error) {
        console.error("Error in compareImages:", error);
        alert("There was an error processing the images.");
    }
}



let filesUploaded = false; // 上传文件标志

// 检查文件上传情况
function checkFileUploaded() {
    const photoAInput = document.getElementById('photoAInput');
    const photoBInput = document.getElementById('photoBInput');

    // 检查是否上传了两张照片
    if (photoAInput.files.length > 0 && photoBInput.files.length > 0) {
        const readerA = new FileReader();
        readerA.onload = function (e) {
            document.getElementById('photoAImage').src = e.target.result;
        };
        readerA.readAsDataURL(photoAInput.files[0]);
        const readerB = new FileReader();
        readerB.onload = function (e) {
            document.getElementById('photoBImage').src = e.target.result;
        };
        readerB.readAsDataURL(photoBInput.files[0]);

        filesUploaded = true; // 设置文件上传标志
        enableDrag(); // 允许拖动功能
    }
}

// 启用拖动功能
function enableDrag() {
    if (filesUploaded) {
        let leftHand = document.getElementById("leftHandArea");
        let rightHand = document.getElementById("rightHandArea");

        leftHand.addEventListener("mousedown", function (e) {
            draggingElement = leftHand;
            offsetX = e.clientX - draggingElement.getBoundingClientRect().left;
            offsetY = e.clientY - draggingElement.getBoundingClientRect().top;

            e.preventDefault();
            document.addEventListener("mousemove", dragMove);
            document.addEventListener("mouseup", stopDrag);
        });

        rightHand.addEventListener("mousedown", function (e) {
            draggingElement = rightHand;
            offsetX = e.clientX - draggingElement.getBoundingClientRect().left;
            offsetY = e.clientY - draggingElement.getBoundingClientRect().top;

            e.preventDefault();
            document.addEventListener("mousemove", dragMove);
            document.addEventListener("mouseup", stopDrag);
        });
    }
}

let draggingElement = null; // 当前被拖动的元素
let offsetX, offsetY;

// 拖动操作
function dragMove(e) {
    if (draggingElement) {
        const left = e.clientX - offsetX;
        const top = e.clientY - offsetY;

        draggingElement.style.left = left + "px";
        draggingElement.style.top = top + "px";
    }
}

// 停止拖动
function stopDrag() {
    document.removeEventListener("mousemove", dragMove);
    document.removeEventListener("mouseup", stopDrag);
    // 获取 leftHand 和 rightHand 的当前位置
    const leftHand = document.getElementById("leftHandArea");
    const rightHand = document.getElementById("rightHandArea");

    // 获取它们的 top 属性值
    const leftTop = parseInt(leftHand.style.top, 10);
    const rightTop = parseInt(rightHand.style.top, 10);

    // 检查两个元素是否都到达 40vh
    if (leftTop <= window.innerHeight * -0.2 && rightTop <= window.innerHeight * -0.2) {
        goToRecommendationPage(); // 调用推荐页面
    }
}


function goToUploadPage() {
    document.querySelector('.hero').style.display = 'none'; // 隐藏首页
    document.querySelector('.upload-page').style.display = 'flex';
    let leftHand = document.getElementById("leftHandArea");
    let rightHand = document.getElementById("rightHandArea");
    leftHand.style.transition = "top 1s ease-in-out";
    rightHand.style.transition = "top 1.5s ease-in-out";
    setTimeout(() => {
        leftHand.style.top = "0";
        rightHand.style.top = "0";
    }, 500);
    setTimeout(() => {
        leftHand.style.transition = "";
        rightHand.style.transition = "";
    }, 3000);
}


// 推荐页面逻辑
function goToRecommendationPage() {
    document.querySelector('.title2').style.display = 'none';
    document.querySelector('.recommendation-page').style.display = 'flex';

    if (filesUploaded) {
        // compareImages();
        generateRandomScores();
        getScoresFromURL();
    } else {
        goToRecommendationPage();
    }

    // 随机推荐分数更高的照片
    setTimeout(() => {
        const hand = document.querySelector('#handImage');
        hand.style.transition = "top 1s ease-in-out, opacity 1s";
        hand.style.top = "5%"; // 移动到目标位置
        hand.style.opacity = "1"; // 显示
    }, 1000);

    setTimeout(() => {
        const hand = document.querySelector('#handImage');
        hand.style.transition = "top 0.5s ease-in-out"; // 短暂移动
        hand.style.top = "-6%"; // 戳一下
    }, 2000);

    setTimeout(() => {
        const hand = document.querySelector('#handImage');
        hand.style.transition = "top 0.5s ease-in-out"; // 回到目标位置
        hand.style.top = "-2%";
        // 显示弹窗
    }, 2800);
    setTimeout(() => {
        const hand = document.querySelector('#handImage');
        hand.style.transition = "top 0.5s ease-in-out"; // 短暂移动
        hand.style.top = "-6%"; // 戳一下
        setTimeout(() => {
            document.getElementById("resultText").innerText =
                scoreA > scoreB ? "I think this one looks better!" : "I think this one looks better!";
            document.getElementById("resultModal").style.display = "block";
        }, 1000);
    }, 3200);
}

// 绑定按钮点击事件来检测文件上传
document.addEventListener('click', checkFileUploaded);