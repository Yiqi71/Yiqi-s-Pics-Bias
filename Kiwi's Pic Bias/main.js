let scoreA = 0;
let scoreB = 0;

function retryUpload() {
    document.getElementById("resultModal").style.display = "none";
    goToUploadPage(); // 回到上传页面
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
    document.getElementById('scoreA').innerText = "Photo A Score: " + scoreA;
    document.getElementById('scoreB').innerText = "Photo B Score: " + scoreB;

    // 根据分数推荐照片
    if (scoreA > scoreB) {
        document.getElementById('handImage').style.left = '30%'; // 推荐 Photo A
    } else {
        document.getElementById('handImage').style.left = '60%'; // 推荐 Photo B
    }
    document.getElementById("recommendation").style.opacity = 0;
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

    generateRandomScores();
    getScoresFromURL();

    // 随机推荐分数更高的照片
    setTimeout(() => {
        const hand = document.querySelector('#handImage');
        hand.style.transition = "top 2s ease-in-out, opacity 2s";
        hand.style.top = "6%"; // 移动到目标位置
        hand.style.opacity = "1"; // 显示
    }, 2000);

    setTimeout(() => {
        const hand = document.querySelector('#handImage');
        hand.style.transition = "top 0.5s ease-in-out"; // 短暂移动
        hand.style.top = "-6%"; // 戳一下
    }, 4000);

    setTimeout(() => {
        const hand = document.querySelector('#handImage');
        hand.style.transition = "top 0.5s ease-in-out"; // 回到目标位置
        hand.style.top = "-2%";
        // 显示弹窗
    }, 4800);
    setTimeout(() => {
        const hand = document.querySelector('#handImage');
        hand.style.transition = "top 0.5s ease-in-out"; // 短暂移动
        hand.style.top = "-6%"; // 戳一下
        setTimeout(() => {
            document.getElementById("resultText").innerText =
                scoreA > scoreB ? "Kiwi prefers the first picture!" : "Kiwi prefers the second picture!";
            document.getElementById("resultModal").style.display = "block";
        }, 1000);
    }, 5200);
}

// 绑定按钮点击事件来检测文件上传
document.addEventListener('click', checkFileUploaded);