from browser import document, html
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def standardize_and_plot(event):
    # 取得輸入值
    x_text = document["x_input"].value
    y_text = document["y_input"].value

    try:
        x_sequence = np.array(list(map(float, x_text.split())))
        y_sequence = np.array(list(map(float, y_text.split())))
        if len(x_sequence) != len(y_sequence) or len(x_sequence) == 0:
            raise ValueError("輸入長度不一致或為空")
    except ValueError:
        document["correlation_result"].text = "請輸入有效數據"
        return

    # 計算標準化
    x_mean, y_mean = np.mean(x_sequence), np.mean(y_sequence)
    x_std, y_std = np.std(x_sequence), np.std(y_sequence)
    x_stdized = (x_sequence - x_mean) / x_std
    y_stdized = (y_sequence - y_mean) / y_std

    correlation = np.corrcoef(x_stdized, y_stdized)[0, 1]

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].scatter(x_sequence, y_sequence, color='blue', label='origin')
    axes[0].axhline(0, color='gray', linestyle='--', linewidth=0.8)
    axes[0].axvline(0, color='gray', linestyle='--', linewidth=0.8)
    axes[0].legend()

    axes[1].scatter(x_stdized, y_stdized, color='red', label='standardization')
    axes[1].axhline(0, color='gray', linestyle='--', linewidth=0.8)
    axes[1].axvline(0, color='gray', linestyle='--', linewidth=0.8)
    axes[1].legend()

    plt.tight_layout()

    # 將圖片轉換為 base64 編碼
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()

    # 更新網頁圖片
    img_element = document["plot_image"]
    img_element.attrs["src"] = f"data:image/png;base64,{img_base64}"

    # 顯示相關係數
    document["correlation_result"].text = f"標準化後的相關係數: {correlation:.4f}"

document["calculate"].bind("click", standardize_and_plot)
