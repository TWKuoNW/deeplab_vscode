import os, random

proportion = 0.9  # 多少比例的圖片當訓練檔
img_dir = "datasets\data\VOCdevkit\VOC2012\JPEGImages"
txt_dir = "datasets\data\VOCdevkit\VOC2012\ImageSets\Segmentation"
os.makedirs(txt_dir, exist_ok=True)
proportion
names = [f[:-4] for f in os.listdir(img_dir) if f.endswith(('.jpg', '.png'))]
random.shuffle(names)
n = len(names)
with open(f"{txt_dir}/train.txt", "w") as f:
    f.writelines(name + "\n" for name in names[:int(n*proportion)])
with open(f"{txt_dir}/val.txt", "w") as f:
    f.writelines(name + "\n" for name in names[int(n*proportion):])
