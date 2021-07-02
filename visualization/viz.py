#==============================================
# 语义分割数据的可视化查看
# 目前已经实现单张图片
# lichuan
# lc@dlc618.com
# 2021.7.2
#==============================================

import matplotlib.pyplot as plt
import cv2


def plot_img_and_mask(img, mask):

    # jpg文件转换为RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # mask文件单通道读取

    classes = mask.shape[2] if len(mask.shape) > 2 else 1
    fig, ax = plt.subplots(1, classes + 1)

    ax[0].set_title('JPG')
    ax[0].imshow(img)
    if classes > 1:
        for i in range(classes):
            ax[i+1].set_title(f'Output mask (class {i+1})')
            ax[i+1].imshow(mask[:, :, i])
    else:
        ax[1].set_title(f'Mask')
        ax[1].imshow(mask)
    
    plt.xticks([]), plt.yticks([])
    plt.show()


if __name__ == '__main__':

    img = cv2.imread('/media/lcq/Data/modle_and_code/DataSet/Segmentation_Dataset_Tools/dataset/aug_jpgs/rs00012_aug_0.jpg')
    mask = cv2.imread('/media/lcq/Data/modle_and_code/DataSet/Segmentation_Dataset_Tools/dataset/aug_masks/rs00012_aug_0.png',0)

    plot_img_and_mask(img, mask)