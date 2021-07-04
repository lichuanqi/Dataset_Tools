#==============================================
# 语义分割数据集的可视化查看
# 目前已经实现单张图片
# lichuan
# lc@dlc618.com
# 2021.7.2
#==============================================

import matplotlib.pyplot as plt
import cv2


def plot_img_and_mask(img, mask):

    # =================================
    # jpg 和 mask 单独显示
    # =================================

    # 根据mask文件的通道数判断类别
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # classes = mask.shape[2] if len(mask.shape) > 2 else 1
    # fig, ax = plt.subplots(1, classes + 1)

    # ax[0].set_title('JPG')
    # ax[0].imshow(img)
    # if classes > 1:
    #     for i in range(classes):
    #         ax[i+1].set_title(f'Output mask (class {i+1})')
    #         ax[i+1].imshow(mask[:, :, i])
    # else:
    #     ax[1].set_title(f'Mask')
    #     ax[1].imshow(mask)
    # plt.xticks([]), plt.yticks([])
    # plt.show()

    # =================================
    # jpg 和 mask 叠加显示
    # =================================
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_fill = img.copy()
    for i in range(len(contours)):
        # 轮廓
        # cv2.drawContours(img, contours[i], -1, (0, 0, 255), 3)
        # 内部填充
        cv2.fillConvexPoly(img_fill, contours[i], (0, 0, 255))
    
    # 按权重叠加
    img_viz = cv2.addWeighted(img, 0.6, img_fill, 0.4, 0)

    cv2.imshow('img',img_viz)
    cv2.waitKey(0)


if __name__ == '__main__':

    
    img = cv2.imread('/media/lcq/Data/modle_and_code/DataSet/Segmentation_Dataset_Tools/dataset/aug_jpgs/rs00012_aug_0.jpg')
    # mask文件单通道读取
    mask = cv2.imread('/media/lcq/Data/modle_and_code/DataSet/Segmentation_Dataset_Tools/dataset/aug_masks/rs00012_aug_0.png',0)

    plot_img_and_mask(img, mask)