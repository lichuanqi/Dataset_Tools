# -*- coding:utf-8 -*-
#===================================================================
# 功能：
#       根据 xml 文件统计目标检测数据集中的类别及数量分布
#       生成训练用的 txt 列表文件
# LICHUAN
# lc@dlc618.com
#===================================================================


import os
import xml.etree.ElementTree as ET
import sys
import time

import numpy as np
np.set_printoptions(threshold=sys.maxsize)
# np.set_printoptions(suppress=True, threshold=np.nan)
import matplotlib
from PIL import Image


def parse_obj(xml_path, filename):
    tree = ET.parse(xml_path + filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        objects.append(obj_struct)
    return objects


def read_image(image_path, filename):
    im = Image.open(image_path + filename)
    W = im.size[0]
    H = im.size[1]
    area = W * H
    im_info = [W, H, area]
    return im_info


if __name__ == '__main__':

    jpg_path = 'E:/MyRails/01/jpgs/'
    xml_path = 'E:/MyRails/01/annos/'
    pre_path = '/data/home/u19120834/DATASET/RailSample/images'

    is_txt = True
    txt_save_path = 'E:/MyRails/01/list.txt'

    if not pre_path:
        pre_path = jpg_path
    
    filenamess = os.listdir(xml_path)
    filenames = []
    txt_list = []
    
    for name in filenamess:
        name = name.replace('.xml', '')
        filenames.append(name)

        txt_list.append(pre_path + name + '.jpg\n')
    
    recs = {}
    obs_shape = {}
    classnames = []
    num_objs = {}
    obj_avg = {}
    
    for i, name in enumerate(filenames):
        recs[name] = parse_obj(xml_path, name + '.xml')
    for name in filenames:
        for object in recs[name]:
            if object['name'] not in num_objs.keys():
                num_objs[object['name']] = 1
            else:
                num_objs[object['name']] += 1
            if object['name'] not in classnames:
                classnames.append(object['name'])
    
    for name in classnames:
        print('{}:{}个'.format(name, num_objs[name]))

    # 生成txt路径文件
    if is_txt == True:
        for image in txt_list:
            with open(txt_save_path, 'a') as t_txt:
                t_txt.write(image)

        print('train.txt is saved')
    
    print('信息统计算完毕。')
    time.sleep(100)

