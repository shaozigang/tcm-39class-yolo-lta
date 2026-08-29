# ===== 步骤1：连接 Google Drive =====
from google.colab import drive
drive.mount('/content/drive')
# 运行后会弹出授权窗口，点"连接到 Google Drive"或"允许"
# 成功标志：打印出 "Mounted at /content/drive"
