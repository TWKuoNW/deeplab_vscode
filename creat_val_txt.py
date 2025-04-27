import os

# 修改成你自己的資料夾路徑（放 .jpg 檔案的資料夾）
image_folder = r'我要測試的資料'  

val_txt_path = os.path.join(image_folder, 'val.txt')
image_names = [os.path.splitext(f)[0] for f in os.listdir(image_folder) if f.lower().endswith('.jpg')]
with open(val_txt_path, 'w') as f:
    for name in sorted(image_names):
        f.write(name + '\n')

print(f"已儲存 {len(image_names)} 筆資料到 val.txt：{val_txt_path}")
