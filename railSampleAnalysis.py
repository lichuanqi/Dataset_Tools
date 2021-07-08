#==============================================
# 样本库数据集数据分析
# lichuan
# lc@dlc618.com
# 2021.7.6
#==============================================

import glob,os

import csv
import numpy as np
from numpy.lib.npyio import save


def get_dir_file(dir_name, pattern = ["*.png","*.jpg","*.jpeg"]):
    '''
    功能
        地区路径下指定后缀的文件路径
    输入
        dir_name ：路径
        pattern  ：文件后缀要求
    输出
        所以符合条件的文件
    '''
    files = []
    for p in pattern:
        for dir,_,_ in os.walk(dir_name):
            files.extend(glob.glob(os.path.join(dir,p)))
    
    return files


def path_split(path='/media/lcq/样本库/铁路标注数据/保定/白天/＜30/平交道口/人/JPEGImages/001903.jpg'):

    path_split = path.split('/')
    img_name = path_split[-1]
    location = path_split[-7]
    sunshine = path_split[-6]
    distance = path_split[-5]
    scene    = path_split[-4]
    target   = path_split[-3]

    keys = [
        # path,
        img_name,
        location,
        sunshine,
        distance,
        scene,
        target]

    return keys


if __name__ == '__main__':
    # 测试路径
    # dir_name = 'dataset/'
    
    # 样本库测试路径
    dir_name = '/media/lcq/样本库/铁路标注数据/保定'
    
    images_path = get_dir_file(dir_name)
    images_num = len(images_path)

    # ===================info ===================
    print('dir path  : {}'.format(dir_name))
    print('file num  : {}'.format(images_num))

    all_keys = []
    csv_headers = [
        'img_name',
        'location',
        'sunshine',
        'distance',
        'scene',
        'target']

    for i in range(images_num):

        keys = path_split(images_path[i])
        all_keys.append(keys)
        # print('--{}/{}:{}'.format(i,images_num,keys))

    with open('example.csv', 'w', newline='') as f: 
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        writer.writerows(all_keys)



