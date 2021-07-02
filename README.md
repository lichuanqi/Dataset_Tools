# Segmentation_Dataset_Tools
语义分割数据集处理相关代码


# 目录结构

```
├── augmentation               # 数据扩张             
│   ├── aug_examples.py        # 语义分割，图片和标签同时扩增
│   ├── aug_image.py           # 单张图片
│   └── aug_original.py       
├── dataset                    # 测试数据集
├── json_to_dataset.py         # LabelMe标注文件转成掩码图片
├── rename.py                  # 文件重命名
├── requirmens.txt
├── split.py                   # 数据集按比例分割为训练集、验证集、测试集
└── visualization              # 数据集可视化
    └── example-vis.py
```