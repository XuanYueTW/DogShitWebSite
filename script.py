from browser import document, html
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def standardize_and_plot(event):
    # 取得輸入值
    x_text = document["x_input"].value
    y_text = document["y_input"].value

    # 轉換數據
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

    # 計算標準化後的相關係數
    correlation = np.corrcoef(x_stdized, y_stdized)[0, 1]

    # 設定圖形範圍
    def get_limits(x, y):
        x_range = (max(x) - min(x)) * 2
        y_range = (max(y) - min(y)) * 2
        limit = max(x_range, y_range) / 2
        x_center, y_center = np.mean(x), np.mean(y)
        return (x_center - limit, x_center + limit), (y_center - limit, y_center + limit)

    (xlim1, xlim2), (ylim1, ylim2) = get_limits(x_sequence, y_sequence)
    (xlim1_std, xlim2_std), (ylim1_std, ylim2_std) = get_limits(x_stdized, y_stdized)

    # **Brython Matplotlib 繪圖修正**
    import matplotlib
    matplotlib.use("Agg")  # 使用非 GUI 後端，確保可在 Brython 中渲染
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # 原始數據圖
    axes[0].scatter(x_sequence, y_sequence, color='blue', label='origin')
    axes[0].axhline(0, color='gray', linestyle='--', linewidth=0.8)
    axes[0].axvline(0, color='gray', linestyle='--', linewidth=0.8)
    axes[0].set_xlim(xlim1, xlim2)
    axes[0].set_ylim(ylim1, ylim2)
    axes[0].legend()
    axes[0].set_aspect('equal')

    # 標準化數據圖
    axes[1].scatter(x_stdized, y_stdized, color='red', label='standardization')
    axes[1].axhline(0, color='gray', linestyle='--', linewidth=0.8)
    axes[1].axvline(0, color='gray', linestyle='--', linewidth=0.8)
    axes[1].set_xlim(xlim1_std, xlim2_std)
    axes[1].set_ylim(ylim1_std, ylim2_std)
    axes[1].legend()
    axes[1].set_aspect('equal')

    plt.tight_layout()

    # 轉換圖形為 base64 圖片
    canvas = FigureCanvas(fig)
    buf = BytesIO()
    canvas.print_png(buf)  # 直接輸出 PNG 圖片
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode()
    buf.close()

    # **顯示圖表**
    document["plot"].clear()
    document["plot"] <= html.IMG(src="data:image/png;base64," + img_base64)

    # **顯示相關係數**
    document["correlation_result"].text = f"標準化後的相關係數: {correlation:.4f}"

# 綁定按鈕事件
document["calculate"].bind("click", standardize_and_plot)
