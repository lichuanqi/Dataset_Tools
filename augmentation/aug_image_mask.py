#coding=utf-8

#==============================================
# 数据增强 - 语义分割数据集
# lichuan
# lc@dlc618.com
# 2021.7.2
#==============================================

import os
from tkinter import image_names

import cv2
from matplotlib import pyplot as plt

from albumentations import (
    Compose,
    OneOf,
    KeypointParams,


    Flip,
    CLAHE,                     # 对比度受限状况下的自适应直方图均衡化算法
    RandomBrightnessContrast,  # 随机选择图片的对比度和亮度
    RandomGamma,               # Gamma变换
    Blur,                      # 滤波
    MotionBlur,                # 运动滤波
    MedianBlur,                # 中值滤波
    ChannelDropout,
    ChannelShuffle,
    RGBShift,
    CoarseDropout,             # 随机填充黑色
    Downscale,                 # 降低分辨率
    Rotate,                    # 旋转
    ShiftScaleRotate,          # 平移/缩放/旋转三合一

    #  未使用
    HorizontalFlip,            # 随机水平翻转
    VerticalFlip,              # 随机垂直翻转
    Resize,                    # 拉伸图片修改尺寸
    PadIfNeeded,
    CenterCrop,
    Crop,
    Transpose,
    ElasticTransform,
    GridDistortion,
    OpticalDistortion,
    RandomSizedCrop,           # 随机尺寸裁剪并缩放回原始大小
    RandomResizedCrop,         # 随机尺寸裁剪并缩放指定大小
    Normalize,                 # 标准化
    )


def data_num(image_path, mask_path):
    #train_img = glob.glob(image_path)
    #masks = glob.glob(mask_path)
    train_img = os.listdir(image_path)
    masks = os.listdir(mask_path)

    return train_img, masks

def mask_aug():
    
    aug = Compose([                
        OneOf([
            RandomGamma(gamma_limit=(40, 140), p=0.5),
            RandomBrightnessContrast(brightness_limit=0.4, contrast_limit=0.4, p=0.5),
            CLAHE(clip_limit=8.0, tile_grid_size=(8, 8), p=0.5),],p=1),
        Flip(p=1),
        CoarseDropout(p=1.0, max_holes=50, max_height=50, max_width=50, min_holes=10, min_height=10, min_width=10),
        ShiftScaleRotate(p=1.0, shift_limit=(-0.3, 0.3), scale_limit=(-0.5, 0.5), rotate_limit=(-40, 40),
                         interpolation=0, border_mode=0),
        ])

    return aug


def mask_one_aug():
    '''
    功能：
        一次只使用一种扩增方式 
    '''
    
    aug = [
        Compose(transforms=[OneOf([
            RandomGamma(gamma_limit=(60, 200), p=0.5),
            RandomBrightnessContrast(brightness_limit=0.5, contrast_limit=0.5, p=0.5),
            CLAHE(clip_limit=6.0, tile_grid_size=(8, 8), p=0.5),
            Blur(blur_limit=7, p=0.5)
            ],p=1)]),

        Compose(transforms=[OneOf([
            ChannelDropout(p=1.0, channel_drop_range=(1, 1), fill_value=0),
            ChannelShuffle(p=1.0),
            RGBShift(p=1.0, r_shift_limit=(-40,40), g_shift_limit=(-40,40), b_shift_limit=(-40,40))
            ],p=1)]),

        Compose(transforms=[
            Flip(p=1)],p=1),

        Compose(transforms=[
            RandomResizedCrop(p=1,height=960,width=960,scale=(0.6,0.9),ratio=(0.75,4))]),
        
        Compose(transforms=[
            CoarseDropout(p=1.0, max_holes=50, max_height=50, max_width=50, min_holes=10, min_height=20, min_width=10)]),
        
        Compose(transforms=[
            Rotate(p=1.0, limit=(-50, 50), interpolation=0, border_mode=0, value=(0, 0, 0))]),
        
        Compose(transforms=[
            ShiftScaleRotate(p=1.0, shift_limit=(-0.1, 0.1), scale_limit=(-0.5, 0.5), rotate_limit=(-20, 20),
                         interpolation=0, border_mode=0)]),

        Compose(transforms=[
            ShiftScaleRotate(p=1.0, shift_limit=(-0.3, 0.3), scale_limit=(-0.3, 0.3), rotate_limit=(-40, 40),
                         interpolation=0, border_mode=0)]),
        ]

    return aug


def main():

    # 测试
    image_path = ('D:/CodePost/Miandan500/test_image/')  # 输入 img 地址
    mask_path = ('D:/CodePost/Miandan500/test_label/')  # 输入 mask 地址
    image_aug_save_path = ('D:/CodePost/Miandan500/train_image_aug/')  # 输入增强img存放地址
    mask_aug_save_path = ('D:/CodePost/Miandan500/train_label_aug/')  # 输入增强mask存放地址
    
    # RailGuard
    # image_path = ('/media/lcq/Data/modle_and_code/DataSet/RailGuard/train/train_image/')  # 输入 img 地址
    # mask_path = ('/media/lcq/Data/modle_and_code/DataSet/RailGuard/train/train_label')  # 输入 mask 地址
    # image_aug_save_path = ('/media/lcq/Data/modle_and_code/DataSet/RailGuard/train/aug_train_image/')  # 输入增强img存放地址
    # mask_aug_save_path = ('/media/lcq/Data/modle_and_code/DataSet/RailGuard/train/aug_train_label/')  # 输入增强mask存放地址

    num = 9  # 输入增强图像增强的张数。

    train_img, masks = data_num(image_path, mask_path)
    # print(train_img)

    # 保存路径如果不存在就新建一个
    if not os.path.exists(image_aug_save_path):
        os.mkdir(image_aug_save_path)
    if not os.path.exists(mask_aug_save_path):
        os.mkdir(mask_aug_save_path)

    image_num = len(train_img)
    print('{:=^50}'.format(' Start '))
    print('Aotal File Number   : {}'.format(image_num))
    print('Augmentation Number : {}'.format(num))

    for data in range(len(train_img)):

        # 文件名
        image_name = train_img[data].split('.')[0]
        print('{}/{}:{}'.format(data+1, image_num, image_name))

        # 绝对路径
        jpg_path_temp = os.path.join(image_path, image_name+'.png')
        print('--', jpg_path_temp)
        mask_path_temp = os.path.join(mask_path, image_name+'.png')

        # 分别读取
        image = cv2.imread(jpg_path_temp)
        mask = cv2.imread(mask_path_temp,0)

        cv2.imwrite(image_aug_save_path + "{}.png".format(image_name), image)
        cv2.imwrite(mask_aug_save_path + "{}.png".format(image_name), mask)

        for i in range(num):
            
            # 每次依次使用所有变换
            # aug = mask_aug()

            # 每次只使用一种变换,当扩增数量大于方法数量时从头开始
            aug = mask_one_aug()
            if i >= len(aug):
                aug = aug[(i%len(aug))]
            else:
                aug = aug[i]

            augmented = aug(image=image, mask=mask)
            aug_image = augmented['image']
            aug_mask = augmented['mask']

            # 保存扩增图片和标签
            cv2.imwrite(image_aug_save_path + "{}_aug_{}.jpg".format(image_name, i+1), aug_image)
            cv2.imwrite(mask_aug_save_path + "{}_aug_{}.png".format(image_name, i+1), aug_mask)

        print('-- Saved')
    
    print('{:=^50}'.format(' End '))


if __name__ == "__main__":
    main()