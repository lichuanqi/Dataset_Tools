#coding=utf-8

#==============================================
# 数据增强 - 单张图片
# lichuan
# lc@dlc618.com
# 2021.6.17
#==============================================


import glob
import tqdm

import cv2
import numpy as np
from matplotlib import pyplot as plt


from albumentations import (
    Compose,
    OneOf,

    Resize,                    # 拉伸图片修改尺寸
    PadIfNeeded,
    HorizontalFlip,            # 随机水平翻转
    VerticalFlip,              # 随机垂直翻转
    CenterCrop,
    Crop,
    Transpose,
    Rotate,        
    ElasticTransform,
    GridDistortion,
    OpticalDistortion,
    
    RandomSizedCrop,           # 随机尺寸裁剪并缩放回原始大小
    RandomResizedCrop,         # 随机尺寸裁剪并缩放指定大小
    CLAHE,                     # 对比度受限状况下的自适应直方图均衡化算法
    Normalize,                 # 标准化
    RandomBrightnessContrast,  # 随机选择图片的对比度和亮度
    RandomGamma,               # Gamma变换
    Blur,                      # 滤波
    MotionBlur,                # 运动滤波
    MedianBlur,                # 中值滤波
    ShiftScaleRotate,          # 平移/缩放/旋转三合一
    Downscale,                 # 降低分辨率
    )


def mask_aug():
    
    aug = Compose([
        OneOf([
            VerticalFlip(p=1.0),
            HorizontalFlip(p=1.0)],p=1),
                
        OneOf([
            RandomGamma(gamma_limit=(80, 120), p=0.5),
            RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
            CLAHE(clip_limit=4.0, tile_grid_size=(4, 4), p=0.5)],p=1),

        OneOf([
            Blur(blur_limit=(7,17), p=0.3),
            MotionBlur(blur_limit=(7,17), p=0.4),
            MedianBlur(blur_limit=(7,17), p=0.3)],p=1),
        
        RandomSizedCrop(min_max_height=(700, 1000), height=1080, width=1920, p=0.8),
        Downscale(p=1.0, scale_min=0.25, scale_max=0.25, interpolation=0),
        Rotate(p=1.0, limit=(-50, 50), interpolation=0, border_mode=0, value=(0, 0, 0), mask_value=None)
        ])

    return aug


def aug_image():
    """
    功能:
        单张图像的增强
    输入:
        NumPy array，channel是RGB
    """
    image_path = '/media/lcq/Data/modle_and_code/DataSet/RailSample/JPEGImages/0002.jpg'
    image_save = '/media/lcq/Data/modle_and_code/DataSet/RailSample/'
    num = 6           # 输入增强图像增强的张数。

    image_name = image_path.split('/')[-1].split('.')[0]

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(image_save + image_name + ".jpg", image)

    for i in range(num):
        aug = mask_aug()[i]
        augmented = aug(image=image)
        image_aug = augmented["image"]

        cv2.imwrite(image_save + image_name + "_aug_{}.jpg".format(i),  image_aug)


if __name__ == "__main__":
    aug_image()

