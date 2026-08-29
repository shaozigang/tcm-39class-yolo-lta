# ===== 步骤2：解压数据集（★这里要改文件名★）=====
import zipfile
import os
import shutil

# ↓↓↓ 把下面这一行的文件名，改成你自己上传到 Drive 里的压缩包真实名字 ↓↓↓
ZIP_PATH = "/content/drive/MyDrive/toxic_herb_dataset.zip"

EXTRACT_DIR = "/content/dataset"

if os.path.exists(EXTRACT_DIR):
    shutil.rmtree(EXTRACT_DIR)
os.makedirs(EXTRACT_DIR, exist_ok=True)

with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(EXTRACT_DIR)

print("解压完成！")
top_items = os.listdir(EXTRACT_DIR)
print("解压后顶层内容：", top_items)

EXPECTED = {"train", "val", "test", "test_subset"}
if EXPECTED.issubset(set(top_items)):
    DATA_ROOT = EXTRACT_DIR
    print(f"结构正常，DATA_ROOT = {DATA_ROOT}")
elif len(top_items) == 1:
    DATA_ROOT = os.path.join(EXTRACT_DIR, top_items[0])
    print(f"检测到多了一层文件夹，已自动修正，DATA_ROOT = {DATA_ROOT}")
else:
    DATA_ROOT = EXTRACT_DIR
    print(f"结构可能异常，请检查，当前 DATA_ROOT = {DATA_ROOT}")
