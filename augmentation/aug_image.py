#coding=utf-8
#==============================================
# 数据增强 - 单张图片
# lichuan
# lc@dlc618.com
# 2021.6.17
#==============================================

import cv2
import numpy as np
from matplotlib import pyplot as plt

from aug_image_mask import mask_aug, mask_one_aug


def aug_image():
    """
    功能:
        单张图像的增强
    输入:
        NumPy array，channel是RGB
    """
    image_path = 'D:/CodePost/Miandan500/train_image/10565.png'
    image_save = 'D:/CodePost/Miandan500/train_image_aug/'
    num = 5           # 输入增强图像增强的张数。

    image_name = image_path.split('/')[-1].split('.')[0]

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 原图复制一份
    cv2.imwrite(image_save + image_name + ".jpg", image)

    for i in range(num):

        # 一次只使用一种数据扩增方法
        aug = mask_one_aug()[i]

        # 一次使用多种数据扩增方法
        # aug = mask_aug()

        augmented = aug(image=image)
        image_aug = augmented["image"]

        cv2.imwrite(image_save + image_name + "_aug_{}.jpg".format(i),  image_aug)

    print('Over')


if __name__ == "__main__":
    aug_image()

