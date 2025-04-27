# 建立結構資料夾
import os

base_path = "datasets//data//VOCdevkit//VOC2012"

# 所有需要的子資料夾
folders = [
    "JPEGImages",
    "SegmentationClass",
    "SegmentationClassOrigin",
    "SegmentationClassAug",  # optional, for trainaug
    "ImageSets/Segmentation"
]

for folder in folders:
    path = os.path.join(base_path, folder)
    os.makedirs(path, exist_ok=True)
    print(f"✅ 建立資料夾：{path}")
