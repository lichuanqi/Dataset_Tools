
# 下载COCO数据集中指定类别的图像和标注
# `list_zoo_datasets` to see the available datasets

import fiftyone as fo
import fiftyone.zoo as foz


# Win10情况下必须把foz.load_zoo_dataset放到main下，否则多进程将会报错
if __name__ == "__main__":  

    dataset = foz.load_zoo_dataset(
        "coco-2017",                 # 指定下载coco-2017类型
        split="validation",          # 指定下载验证集
        label_types=["detections"],  # 指定下载目标检测的类型
        classes=["train"],           # 指定下载猫的类别
        max_samples=150,              # 指定下载符合条件的最大样本数
        only_matching=True,          # 指定仅下载符合条件的图片，即含有猫的图片
        num_workers=1,               # 指定进程数为1
        dataset_dir="D:/Code/DATASET/5151",    
        dataset_name="open-c",       # 指定新下载的数据集的名称,会检测是否已有,不同的dataset 都是指向了同一个原始图像的路径
    )
    session = fo.launch_app(dataset)
    session.wait()  #