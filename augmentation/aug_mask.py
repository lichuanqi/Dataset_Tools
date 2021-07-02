#coding=utf-8

#==============================================
# 数据增强 - 语义分割数据集
# lichuan
# lc@dlc618.com
# 2021.7.2
#==============================================

import os

import cv2
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
    ShiftScaleRotate,          # 平移/缩放/旋转三合一
    Downscale,                 # 降低分辨率
    Rotate,                    # 旋转
    )


def data_num(train_path, mask_path):
    #train_img = glob.glob(train_path)
    #masks = glob.glob(mask_path)
    train_img = os.listdir(train_path)
    masks = os.listdir(mask_path)

    return train_img, masks

def mask_aug():
    
    aug = Compose([
        OneOf([
            VerticalFlip(p=1.0),
            HorizontalFlip(p=1.0)],p=1),
                
        OneOf([
            RandomGamma(gamma_limit=(80, 120), p=0.5),
            RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
            CLAHE(clip_limit=4.0, tile_grid_size=(4, 4), p=0.5),],p=1),
        
        OneOf([
            Blur(blur_limit=5, p=1),
            MotionBlur(blur_limit=5, p=1),
            MedianBlur(blur_limit=5, p=1),],p=1),
        
        RandomSizedCrop(min_max_height=(700, 1000), height=1080, width=1920, p=1),
        Downscale(p=1.0, scale_min=0.25, scale_max=0.25, interpolation=0),
        Rotate(p=1.0, limit=(-40, 40), interpolation=0, border_mode=0, value=(0, 0, 0), mask_value=None)
        ])

    return aug

def main():

    # 测试
    # train_path = ('/media/lcq/Data/modle_and_code/DataSet/Segmentation_Dataset_Tools/dataset/jpgs/')  # 输入 img 地址
    # mask_path = ('/media/lcq/Data/modle_and_code/DataSet/Segmentation_Dataset_Tools/dataset/masks/')  # 输入 mask 地址
    # augtrain_path = ('/media/lcq/Data/modle_and_code/DataSet/Segmentation_Dataset_Tools/dataset/aug_jpgs/')  # 输入增强img存放地址
    # augmask_path = ('/media/lcq/Data/modle_and_code/DataSet/Segmentation_Dataset_Tools/dataset/aug_masks/')  # 输入增强mask存放地址
    
    # RailGuard
    train_path = ('/media/lcq/Data/modle_and_code/DataSet/RailGuard200/jpgs/')  # 输入 img 地址
    mask_path = ('/media/lcq/Data/modle_and_code/DataSet/RailGuard200/masks/')  # 输入 mask 地址
    augtrain_path = ('/media/lcq/Data/modle_and_code/DataSet/RailGuard200/aug_jpgs/')  # 输入增强img存放地址
    augmask_path = ('/media/lcq/Data/modle_and_code/DataSet/RailGuard200/aug_masks/')  # 输入增强mask存放地址

    num = 6  # 输入增强图像增强的张数。

    train_img, masks = data_num(train_path, mask_path)
    # print(train_img)

    print('================ Start ================')
    print('Aotal File Number   : {}'.format(len(train_img)))
    print('Augmentation Number : {}'.format(num))

    for data in range(len(train_img)):

        # 绝对路径
        jpg_path_temp = os.path.join(train_path, train_img[data])
        mask_path_temp = os.path.join(mask_path, masks[data])

        # 文件名
        image_name = train_img[data].split('.')[0]
        # print(image_name)

        # 分别读取
        image = cv2.imread(jpg_path_temp)
        mask = cv2.imread(mask_path_temp,0)

        cv2.imwrite(augtrain_path + "{}.jpg".format(image_name), image)
        cv2.imwrite(augmask_path + "{}.png".format(image_name), mask)


        for i in range(0,num):
            
            aug = mask_aug()[i]
            augmented = aug(image=image, mask=mask)
            aug_image = augmented['image']
            aug_mask = augmented['mask']

            # 保存扩增图片和标签
            cv2.imwrite(augtrain_path + "{}_aug_{}.jpg".format(image_name, i), aug_image)
            cv2.imwrite(augmask_path + "{}_aug_{}.png".format(image_name, i), aug_mask)

        print('{}/{}: {} Saved'.format(data+1,len(train_img),image_name))
    
    print('================  End  ================')


if __name__ == "__main__":
    main()
