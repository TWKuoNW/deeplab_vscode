第一步:
生成結構性資料夾，執行 creat_folder.py

第二步:
把訓練資料放入
圖片 -> "datasets\JPEGImages"
標記 -> "datasets\SegmentationClass" (請放binary的照片，並且檔名要與圖片一致；如何轉換請參考UNet的方法)

第三步:
生成.txt文件，目的是為了分類那些要做訓練那些要做驗證，執行 creat_txt.py

第四步:
開始訓練，訓練命令如下，複製貼到終端機：
python main.py --model deeplabv3plus_mobilenet --year 2012 --crop_val --crop_size 513 --lr 0.01 --batch_size 10 --output_stride 16 --gpu_id 0 --total_itrs 30000 --val_interval 10 --log_name log_1

第五步:
開始測試
python main.py --model deeplabv3plus_mobilenet --year 2012 --batch_size 1 --output_stride 16 --gpu_id 0 --ckpt checkpoints\best_seagrass_ver1.pth --test_only --save_val_results --data_root ./datasets/data --num_classes 2
