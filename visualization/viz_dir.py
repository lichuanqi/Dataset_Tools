#==============================================
# 语义分割数据集的可视化查看
# 查看文件夹内所以数据
# lichuan
# lc@dlc618.com
# 2021.7.2
#==============================================

import matplotlib.pyplot as plt
import cv2

import os,glob

def get_filename(jpg_dir, masks_dir):

    jpgs = os.listdir(jpg_dir)
    masks = os.listdir(masks_dir)

    return jpgs, masks


def show_all(jpg_dir, masks_dir):

    jpgs, masks = get_filename(jpg_dir, masks_dir)
    current, key = 0, ord('a')

    print('======================== Start ========================')
    print('jpgs path  : {}'.format(jpg_dir))
    print('jpgs num   : {}'.format(len(jpgs)))
    print('jpgs names : {}'.format(jpgs))

    while key > ord(' '):
        
        name_temp = jpgs[current].split('.')[0]
        jpg_temp = os.path.join(jpg_dir, '{}.jpg'.format(name_temp))
        mask_temp = os.path.join(masks_dir, '{}{}.png'.format(name_temp,name_post))

        jpg = cv2.imread(jpg_temp)
        mask = cv2.imread(mask_temp, 0)

        contours, hie = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img_fill = jpg.copy()
        for ci in range(len(contours)):
            # 轮廓
            # cv2.drawContours(img, contours[i], -1, (0, 0, 255), 3)
            # 内部填充
            cv2.fillConvexPoly(img_fill, contours[ci], (0, 0, 255))
    
        # 按权重叠加
        img_add = cv2.addWeighted(jpg, 0.6, img_fill, 0.4, 0)
        text = '{}/{}: {}'.format(current+1, len(jpgs), name_temp)
        cv2.putText(img_add, text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 2)
        
        cv2.imshow('Windows', img_add)

        #use 'a' and 'd' to scroll through frames
        key = cv2.waitKey(-1) 
        current = current - 1 if key == ord('a') else current + 1
        current = (current + len(jpgs)) % len(jpgs) #wrap around
    
    return 0

if __name__=='__main__':

    # 测试路径
    jpg_dir = '/media/lcq/Data/modle_and_code/DataSet/Dataset_Tools/dataset/aug_jpgs'
    masks_dir = '/media/lcq/Data/modle_and_code/DataSet/Dataset_Tools/dataset/aug_masks'
    name_post = ''

    # RailGuard
    # jpg_dir   = '/media/lcq/Data/modle_and_code/DataSet/RailGuard200/aug_jpgs'
    # masks_dir = '/media/lcq/Data/modle_and_code/DataSet/RailGuard200/aug_ masks'
    # name_post = ''

    # output
    # jpg_dir   = '/media/lcq/Data/modle_and_code/python_cnn/Keras-Semantic-Segmentation/data/RailGuard/test/'
    # masks_dir = '/media/lcq/Data/modle_and_code/python_cnn/Keras-Semantic-Segmentation/data/RailGuard/output-0709/'
    # name_post = '_unet'
    
    show_all(jpg_dir, masks_dir)

