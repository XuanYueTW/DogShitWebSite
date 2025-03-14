document.getElementById("press").addEventListener("click", function() {
    document.getElementById("CaoNiMaVideo").play();
    document.getElementById("press").style.display = "none";
    document.getElementById("videoContainer").style.display = "block";
    document.getElementById("CaoNiMaVideo").style.display = "block";
    document.getElementById("CaoNiMaVideo").muted = false;
});

let rippleCount = 0;
let rippleCountDisplay = document.createElement("div");
rippleCountDisplay.style.position = "absolute";
rippleCountDisplay.style.top = "10px";
rippleCountDisplay.style.left = "10px";
rippleCountDisplay.style.fontSize = "20px";
rippleCountDisplay.style.color = "white";
rippleCountDisplay.style.zIndex = "9999";
document.body.appendChild(rippleCountDisplay);

function updateRippleCountDisplay() {
    rippleCountDisplay.textContent = `cps: ${rippleCount}`;
    if (rippleCount < 1) {
        rippleCountDisplay.style.display = "none";
    } else {
        rippleCountDisplay.style.display = "block";
    }
}

document.documentElement.addEventListener("click", function(event) {
    let ripple = document.createElement("div");
    ripple.classList.add("ripple");

    ripple.style.left = `${event.pageX - 5}px`;
    ripple.style.top = `${event.pageY - 5}px`;

    document.documentElement.appendChild(ripple);
    rippleCount++;
    updateRippleCountDisplay();

    setTimeout(() => {
        ripple.remove();
        rippleCount--;
        updateRippleCountDisplay();
    }, 1000);
});

function updateDateTime() {
    let now = new Date();
    let year = now.getFullYear();
    let month = now.getMonth() + 1;
    let day = now.getDate();
    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();

    month = month.toString().padStart(2, '0');
    day = day.toString().padStart(2, '0');
    hours = hours.toString().padStart(2, '0');
    minutes = minutes.toString().padStart(2, '0');
    seconds = seconds.toString().padStart(2, '0');

    let dateTimeString = `${year} 年 ${month} 月 ${day} 日 ${hours}:${minutes}:${seconds}`;

    document.getElementById("timeDisplay").textContent = dateTimeString;
}

let startTime = Date.now();

function updateElapsedTime() {
    let elapsedTime = Math.floor((Date.now() - startTime) / 1000);

    let displayText = `你在這裡浪費了: ${elapsedTime} 秒`;

    let seconds = elapsedTime % 60;
    let minutes = Math.floor(elapsedTime / 60) % 60;
    let hours = Math.floor(elapsedTime / 3600) % 24;
    let days = Math.floor(elapsedTime / 86400) % 365;
    let years = Math.floor(elapsedTime / 31536000);

    if (elapsedTime >= 60) {
        displayText = `你在這裡浪費了: ${minutes} 分 ${seconds} 秒`;

        if (elapsedTime >= 3600) {
            displayText = `你在這裡浪費了: ${hours} 小時 ${minutes} 分 ${seconds} 秒`;

            if (elapsedTime >= 86400) {
                displayText = `你在這裡浪費了: ${days} 天 ${hours} 小時 ${minutes} 分 ${seconds} 秒`;

                if (elapsedTime >= 31536000) {
                    displayText = `你在這裡浪費了: ${years} 年 ${days} 天 ${hours} 小時 ${minutes} 分 ${seconds} 秒`;
                }
            }
        }
    }

    document.getElementById("ElapsedtimeDisplay").textContent = displayText;
}

setInterval(updateElapsedTime, 1000);
setInterval(updateDateTime, 1000);
updateElapsedTime();
updateDateTime();