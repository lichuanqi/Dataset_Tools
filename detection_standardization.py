#==============================================
# 目标检测数据集的标准化
# 利用数据扩增的随机剪裁将数据集的尺寸统一为标准尺寸
# lichuan
# lc@dlc618.com
# 2021.8.23
#==============================================

import os,glob
import time
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOC

import cv2
import numpy as np
from matplotlib import pyplot as plt

from albumentations import (
    Compose,
    OneOf,
    BboxParams,

    RandomSizedCrop,
    )


def data_num(train_path, mask_path):
    '''
    功能：
        从xml文件中提取bounding box信息
    输入：
        xml_path: xml的文件路径
    输出：
        从xml文件中提取bounding box信息, 
        [[x_min, y_min, width, height]]
        [lables]
    '''
    train_img = os.listdir(train_path)
    masks = os.listdir(mask_path)

    return train_img, masks


def parse_xml(xml_path):
    '''
    功能：
        从xml文件中提取 bounding box 信息
    输入：
        xml_path: xml 文件路径
    输出：
        bounding box 信息, 格式为 [[x_min, y_min, width, height, lables]]
    '''
    tree = ET.parse(xml_path)
    root = tree.getroot()
    objs = root.findall('object')

    coords = list()
    
    for ix, obj in enumerate(objs):
        name = obj.find('name').text
        box = obj.find('bndbox')
        x_min = int(box[0].text)
        y_min = int(box[1].text)
        x_max = int(box[2].text)
        y_max = int(box[3].text)
        width  = int(box[2].text) - int(box[0].text)
        height = int(box[3].text) - int(box[1].text)
        coords.append([x_min, y_min, width, height, name])

    return coords


def generate_xml(img_name,coords,img_size,aug_xml_temp):
    '''
    功能：
        将bounding box信息写入xml文件中,
    输入：
        img_name     ：图片名称，如 a.jpg
        coords       : 坐标list，格式为 [[x_min, y_min, x_max, y_max, labels]]
        img_size     ：图像的大小,格式为 [h,w,c]
        aug_xml_temp : xml文件输出的路径和名称
    '''
    doc = DOC.Document()  # 创建DOM文档对象

    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    title = doc.createElement('folder')
    title_text = doc.createTextNode('Tianchi')
    title.appendChild(title_text)
    annotation.appendChild(title)

    title = doc.createElement('filename')
    title_text = doc.createTextNode(img_name)
    title.appendChild(title_text)
    annotation.appendChild(title)

    source = doc.createElement('source')
    annotation.appendChild(source)

    title = doc.createElement('database')
    title_text = doc.createTextNode('The Tianchi Database')
    title.appendChild(title_text)
    source.appendChild(title)

    title = doc.createElement('annotation')
    title_text = doc.createTextNode('Tianchi')
    title.appendChild(title_text)
    source.appendChild(title)

    size = doc.createElement('size')
    annotation.appendChild(size)

    title = doc.createElement('width')
    title_text = doc.createTextNode(str(img_size[1]))
    title.appendChild(title_text)
    size.appendChild(title)

    title = doc.createElement('height')
    title_text = doc.createTextNode(str(img_size[0]))
    title.appendChild(title_text)
    size.appendChild(title)

    title = doc.createElement('depth')
    title_text = doc.createTextNode(str(img_size[2]))
    title.appendChild(title_text)
    size.appendChild(title)

    for coord in coords:

        object = doc.createElement('object')
        annotation.appendChild(object)

        title = doc.createElement('name')
        title_text = doc.createTextNode(coord[4])
        title.appendChild(title_text)
        object.appendChild(title)

        pose = doc.createElement('pose')
        pose.appendChild(doc.createTextNode('Unspecified'))
        object.appendChild(pose)
        truncated = doc.createElement('truncated')
        truncated.appendChild(doc.createTextNode('1'))
        object.appendChild(truncated)
        difficult = doc.createElement('difficult')
        difficult.appendChild(doc.createTextNode('0'))
        object.appendChild(difficult)

        bndbox = doc.createElement('bndbox')
        object.appendChild(bndbox)
        title = doc.createElement('xmin')
        title_text = doc.createTextNode(str(int(float(coord[0]))))
        title.appendChild(title_text)
        bndbox.appendChild(title)
        title = doc.createElement('ymin')
        title_text = doc.createTextNode(str(int(float(coord[1]))))
        title.appendChild(title_text)
        bndbox.appendChild(title)
        title = doc.createElement('xmax')
        title_text = doc.createTextNode(str(int(float(coord[2]))))
        title.appendChild(title_text)
        bndbox.appendChild(title)
        title = doc.createElement('ymax')
        title_text = doc.createTextNode(str(int(float(coord[3]))))
        title.appendChild(title_text)
        bndbox.appendChild(title)

    # 将DOM对象doc写入文件
    f = open(aug_xml_temp,'w')
    f.write(doc.toprettyxml(indent = ''))
    f.close()


def mask_aug():
    '''
    功能：
        随机剪裁并缩放到指定尺寸
    '''

    aug = Compose(transforms=[
        
        RandomSizedCrop(p=1,min_max_height=(900,1000),height=640,width=640,w2h_ratio=1),],

        p=1,bbox_params = BboxParams(format='coco', min_area=50, min_visibility=0.7))

    return aug


def main():

    # 测试
    # img_path = ('/media/lcq/Data/modle_and_code/DataSet/Dataset_Tools/dataset/detection/anno/')         # 要扩增的 jpg 路径
    # xml_path = ('/media/lcq/Data/modle_and_code/DataSet/Dataset_Tools/dataset/detection/xml/')          # 要扩增的 xml 路径
    # aug_img_path = ('/media/lcq/Data/modle_and_code/DataSet/Dataset_Tools/dataset/detection/aug_anno/') # 扩增后的 jpg 路径
    # aug_xml_path = ('/media/lcq/Data/modle_and_code/DataSet/Dataset_Tools/dataset/detection/aug_xml/')  # 扩增后的 xml 路径
    
    # ICIG
    img_path = ('/media/lcq/Data/项目/2019-空天车地/20210822-结题材料/目标检测数据集-500张图片/JPEGImages/')
    xml_path = ('/media/lcq/Data/项目/2019-空天车地/20210822-结题材料/目标检测数据集-500张图片/Annotations/')
    aug_img_path = ('/media/lcq/Data/项目/2019-空天车地/20210822-结题材料/目标检测数据集-500张图片/JPEGImages-new/')
    aug_xml_path = ('/media/lcq/Data/项目/2019-空天车地/20210822-结题材料/目标检测数据集-500张图片/Annotations-new/')

    # 图像增强数量
    num = 1

    # 读取指定文件夹内的文件路径
    imgs, xmls = data_num(img_path, xml_path)

    start_time = time.time()
    print('================ Start ================')
    print('Aotal File Number   : {}'.format(len(imgs)))
    print('Augmentation Number : {}'.format(num))

    for data in range(len(imgs)):

        # 文件名
        image_name = imgs[data].split('.')[0]

        # 绝对路径
        jpg_path_temp = os.path.join(img_path, image_name+'.jpg')
        xml_path_temp = os.path.join(xml_path, image_name+'.xml')

        # 分别读取图片和标签文件
        image = cv2.imread(jpg_path_temp)
        boxes = parse_xml(xml_path_temp)

        for i in range(0,num):
            
            aug = mask_aug()                         

            augmented = aug(image=image, bboxes=boxes)
            aug_image = augmented['image']
            aug_boxes = augmented['bboxes']

            # 将标签数据标准为 [[xmin,ymin,xmax,ymax,labels]]
            coords = list()
            for box in aug_boxes:
                coords.append([box[0],box[1],box[2]+box[0],box[3]+box[1], box[4]])

            # 保存扩增图片和标签
            cv2.imwrite(aug_img_path + "{}_aug_{}.jpg".format(image_name, i), aug_image)
            aug_xml_temp = aug_xml_path + "{}_aug_{}.xml".format(image_name, i)
            img_size = image.shape
            generate_xml(image_name,coords,img_size,aug_xml_temp)

        print('{}/{}: {} Finshed and Saved.'.format(data+1,len(imgs),image_name))
    
    print('Time Used          : {:.3f}s'.format(time.time() - start_time))
    print('================  End  ================')

if __name__ == "__main__":
    main()