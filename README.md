# Dataset_Tools
深度学习数据集处理相关代码

目标检测和语义分割

# 目录结构

```
├── analysis                   # 数据集分析
│   └── classDistribution.py   # 统计目标检测数据集类别及数量
├── augmentation               # 数据扩增             
│   ├── aug_examples.py        
│   ├── aug_image.py           # 单张图片
│   ├── aug_detection.py       # 目标检测，图片和标签同时
│   └── aug_mask.py            # 语义分割，图片和掩码同时
├── dataset                    # 测试数据集
│   ├── detection
│   ├── aug_jpgs
│   ├── aug_masks
│   ├── jpgs
│   ├── jsons
│   ├── masks
│   └── viz
├── json_to_dataset.py         # LabelMe标注文件转成掩码图片
├── xml2yolo.py                # LabelImg 标注的 xml 数据转化为 YOLO 所用的 TXT 数据
├── rename.py                  # 文件重命名
├── split.py                   # 数据集按比例分割为训练集、验证集、测试集
├── railSampleAnalysis.py      # 样本库分析
└── visualization              # 语义分割数据集可视化查看
    ├── example-vis.py
    ├── viz_dir.py             # 查看文件夹内所有图片
    └── viz_image.py           # 查看单张图片

```

# Requirments

- numpy
- opencv-pyhton
- albumentations

安装，缺啥补啥`pip install numpy opencv-pyhton albumentations`