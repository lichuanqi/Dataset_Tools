# Dataset_Tools
目标检测和语义分割数据集处理相关工具代码



# 目录结构

```
├── 5151                   # FiftyOne数据集可视化工具测试
│   └── coco_down.py           # 下载coco数据集指定类别的图片
├── analysis                   # 数据集分析
│   ├── class_statistics.py    # 统计目标检测数据集类别及数量
│   ├── coco_statistics.py     # 统计COCO数据集各个类别的图片数和标注框数
├── augmentation           # 数据扩增             
│   ├── aug_examples.py        
│   ├── aug_image.py           # 单张图片
│   ├── aug_detection.py       # 目标检测，图片和标签同时
│   └── aug_mask.py            # 语义分割，图片和掩码同时
├── dataset                # 测试数据集
│   ├── detection
│   ├── aug_jpgs
│   ├── aug_masks
│   ├── jpgs
│   ├── jsons
│   ├── masks
│   └── viz
├── format_convert         # 数据集格式相互转换
│   ├── coco2xml.py
│   ├── coco2yolo.py
│   ├── dataset_names.py       # 常用数据集类别列表
│   ├── json2xml.py            
│   ├── xml2yolo.py            # LabelImg 标注的 xml 数据转化为 YOLO 所用的 TXT 数据
│   ├── json_to_dataset.py     # LabelMe标注文件转成掩码图片      
├── anchors_by_kmeans.py       # kmeans聚类获取先验框大小
├── rename.py                  # 文件重命名
├── split_train_val.py         # 数据集按比例分割为训练集、验证集、测试集
├── select_by_xml.py           # 根据xml数据挑选包含指定类别的图片数据，并按照一定格式重命名。
├── railSampleAnalysis.py      # 样本库分析
├── detection_standardization.py   # 利用数据扩增的随机剪裁将数据集的尺寸统一为标准尺寸
└── visualization         # 标注数据可视化查看
    ├── xml_viz_img.py         # xml标注数据可视化
    ├── txt_viz_img.py         # txt标注数据可视化
    ├── example-vis.py
    ├── png_viz_dir.py         # png可视化，查看文件夹内所有图片
    └── png_viz_img.py       # png可视化，查看单张图片

```


# Requirments

- numpy
- opencv-pyhton
- albumentations

安装，缺啥补啥`pip install numpy opencv-pyhton albumentations`