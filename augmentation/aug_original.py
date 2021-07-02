#coding=utf-8

#==============================================
# 数据增强 - 语义分割
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
    RandomRotate90,            # 随机90度旋转
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
    ShiftScaleRotate           # 平移/缩放/旋转三合一
    )

def data_num(train_path, mask_path):
    train_img = glob.glob(train_path)
    masks = glob.glob(mask_path)
    return train_img, masks

def mask_aug():
    
    aug = Compose([
        # VerticalFlip(p=0.5),
        HorizontalFlip(p=0.5),
        RandomSizedCrop(min_max_height=(600, 1000), height=1080, width=1920, p=0.5),
        Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, p=1.0),
        
        OneOf([
            # RandomGamma(gamma_limit=(60, 120), p=0.5),
            RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
            CLAHE(clip_limit=4.0, tile_grid_size=(4, 4), p=0.5)]),
        
        OneOf([
            Blur(blur_limit=5, p=1),
            MotionBlur(blur_limit=5, p=1),
            MedianBlur(blur_limit=5, p=1)]),
        
        ShiftScaleRotate(shift_limit=0.2, scale_limit=0.2, rotate_limit=20),
        ])

    return aug

def main():

    train_path = ('/media/lcq/Data/modle_and_code/python_cnn/Pytorch-UNet/predict.py')  # 输入 img 地址
    mask_path = ('/media/lcq/Data/modle_and_code/DataSet/DatasetTools/dataset/masks_test/rs00012.png')  # 输入 mask 地址
    augtrain_path = ('/media/lcq/Data/modle_and_code/DataSet/DatasetTools/dataset/jpgs_aug')  # 输入增强img存放地址
    augmask_path = ('/media/lcq/Data/modle_and_code/DataSet/DatasetTools/dataset/masks_aug')  # 输入增强mask存放地址
    num = 3  # 输入增强图像增强的张数。
    aug = mask_aug()

    train_img, masks = data_num(train_path, mask_path)

    for data in range(len(train_img)):
        for i in range(num):
            image = cv2.imread(train_img[data])
            mask = cv2.imread(masks[data])
            augmented = aug(image=image, mask=mask)
            aug_image = augmented['image']
            aug_mask = augmented['mask']
            cv2.imwrite("./data/data-2/new_image/aug{}_{}.jpg".format(data, i), aug_image)
            cv2.imwrite("./data/data-2/new_label/aug{}_{}.png".format(data, i), aug_mask)
            print(data)
# cv2.imshow("x",aug_image)
# cv2.imshow("y",aug_mask)
# cv2.waitKey(0)


def aug_image():
    """
    功能:
        单张图像的增强
    输入:
        NumPy array，channel是RGB
    """
    image_path = '/media/lcq/Data/modle_and_code/DataSet/RailSample/JPEGImages/0002.jpg'
    image_save = '/media/lcq/Data/modle_and_code/DataSet/RailSample/JPEGImages_aug/'
    num = 3           # 输入增强图像增强的张数。

    image_name = image_path.split('/')[-1].split('.')[0]

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.array(image)
    
    for i in range(num):

        aug = mask_aug()
        image_aug = aug(image=image)["image"]
        
        print(image_aug)
        cv2.imshow('s',image_aug)
        cv2.imwrite(image_save + image_name + "_aug_{}.jpg".format(i),  image_aug)

        cv2.waitKey(100)


if __name__ == "__main__":
    # main()
    aug_image()

