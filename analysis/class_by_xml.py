# -*- coding:utf-8 -*-
#===================================================================
# 功能：
#       统计目标检测数据集类别分布情况
# LICHUAN
# lc@dlc618.com
#===================================================================


from cProfile import label
import os
from pickle import OBJ
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

    jpg_path = 'D:/CodePost/Xray_select/jpgs/'
    xml_path = 'D:/CodePost/Xray_select/xmls/'

    # 将结果保存为txt文件
    save_txt = True
    save_path = ''
    txt_path = save_path + 'list.txt'
    label_path = save_path + 'label.txt'
    
    xmls = os.listdir(xml_path)       # xml文件绝对路径
    names = []                        # 不包含扩展名的文件名
    jpgs = []                         # jpg文件绝对路径
    
    # 保存文件名列表
    for xml in xmls:
        name = xml.replace('.xml', '')
        names.append(name)
        jpgs.append(jpg_path + name + '.jpg\n')

    print('共读取 {} 条xml数据。'.format(len(xmls)))
    
    recs = {}
    classnames = []                # 目标名称
    num_objs = {}                  # 目标名称及数量
    
    # 遍历一下所有图片读取所有目标名称
    for i, name in enumerate(names):
        recs[name] = parse_obj(xml_path, name + '.xml')

    for name in names:
        for object in recs[name]:
            if object['name'] not in num_objs.keys():
                num_objs[object['name']] = 1
            else:
                num_objs[object['name']] += 1

            if object['name'] not in classnames:
                classnames.append(object['name'])
    
    print('信息统计算完毕：')
    for name in classnames:
        print('--{: <15}: {}'.format(name, num_objs[name]))

    # 生成txt路径文件
    if save_txt == True:
        # for image in jpgs:
        #     with open(txt_path, 'a') as t_txt:
        #         t_txt.write(image)

        with open (label_path, 'a') as label:
            label.write('共读取 {} 条xml数据。\n'.format(len(xmls)))
            for name in classnames:
                label.write(name + ': ' + str(num_objs[name]) + '\n')

        print('txt saved')
    

    time.sleep(100)

