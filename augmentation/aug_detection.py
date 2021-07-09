#==============================================
# 数据增强 - 目标检测数据集
# lichuan
# lc@dlc618.com
# 2021.7.9
# ref:https://blog.csdn.net/qq_43555843/article/details/103577196
#==============================================

import os,glob
import time
import shutil
import random
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOC

import cv2
import numpy as np
from matplotlib import pyplot as plt

from albumentations import (
    Compose,
    OneOf,
    BboxParams,

    ChannelDropout,
    ChannelShuffle,
    RGBShift,
    Flip,                      # 水平、垂直或同时水平和垂直翻转
    CLAHE,                     # 对比度受限状况下的自适应直方图均衡化算法
    RandomBrightnessContrast,  # 随机选择图片的对比度和亮度
    RandomGamma,               # Gamma变换
    Blur,                      # 滤波
    MotionBlur,                # 运动滤波
    MedianBlur,                # 中值滤波
    Downscale,                 # 降低分辨率
    RandomResizedCrop,         # 剪裁并缩放
    Rotate,                    # 旋转
    ShiftScaleRotate,          # 平移/缩放/旋转三合一

    #  未使用
    HorizontalFlip,            # 随机水平翻转
    VerticalFlip,              # 随机垂直翻转
    CropAndPad,                # 剪裁并填充
    CoarseDropout,             # 随机填充黑色，目标检测不能用
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


def data_num(train_path, mask_path):
    #train_img = glob.glob(train_path)
    #masks = glob.glob(mask_path)
    train_img = os.listdir(train_path)
    masks = os.listdir(mask_path)

    return train_img, masks


def parse_xml(xml_path):
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
    tree = ET.parse(xml_path)
    root = tree.getroot()
    objs = root.findall('object')

    coords = list()
    labels = list()
    
    for ix, obj in enumerate(objs):
        name = obj.find('name').text
        box = obj.find('bndbox')
        x_min = int(box[0].text)
        y_min = int(box[1].text)
        x_max = int(box[2].text)
        y_max = int(box[3].text)
        width  = int(box[2].text) - int(box[0].text)
        height = int(box[3].text) - int(box[1].text)
        # coords.append([x_min, y_min, width, height])
        # labels.append(name)
        coords.append([x_min, y_min, width, height, name])
    return coords


def generate_xml(img_name,coords,img_size,aug_xml_temp):
    '''
    功能：
        将bounding box信息写入xml文件中,
    输入：
        img_name     ：图片名称，如a.jpg
        coords       : 坐标list，格式为[[x_min, y_min, x_max, y_max, name]]
        img_size     ：图像的大小,格式为[h,w,c]
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
        每一次都使用所有的扩增方式 
    '''

    aug = Compose(transforms=[
        OneOf([
            RandomGamma(gamma_limit=(80, 120), p=1),
            RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=1),
            CLAHE(clip_limit=4.0, tile_grid_size=(4, 4), p=1),],
            p=0.5),
        
        OneOf([
            Blur(blur_limit=5, p=1),
            MotionBlur(blur_limit=5, p=1),
            MedianBlur(blur_limit=5, p=1),],
            p=0.5),
        
        OneOf([
            ChannelDropout(p=1.0, channel_drop_range=(1, 1), fill_value=0),
            ChannelShuffle(always_apply=False, p=1.0),
            RGBShift(p=1.0, r_shift_limit=(-40,40), g_shift_limit=(-40,40), b_shift_limit=(-40,40))
            ],p=0.5),

        Flip(p=0.5),
        RandomResizedCrop(p=0.5,height=1080,width=1920,scale=(0.6,0.9),ratio=(0.75,4)),
        Rotate(p=0.5, limit=(-40, 40), interpolation=0, border_mode=0, value=(0, 0, 0)),
        ShiftScaleRotate(p=0.5, shift_limit=(-0.05, 0.05), scale_limit=(-0.5, 0.5), rotate_limit=(-20, 20)),
        ShiftScaleRotate(p=0.5, shift_limit=(-0.25, 0.25), scale_limit=(-0.1, 0.1), rotate_limit=(-20, 20))
        ],p=1,
        bbox_params = BboxParams(format='coco', min_area=50, min_visibility=0.7))

    return aug


def mask_one_aug():
    '''
    功能：
        一次只使用一种扩增方式 
    '''
    bbox_params = BboxParams(format='coco', min_area=50, min_visibility=0.7)
    
    aug = [Compose(transforms=[OneOf([
            RandomGamma(gamma_limit=(80, 120), p=1),
            RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=1),
            CLAHE(clip_limit=4.0, tile_grid_size=(4, 4), p=1),],
            p=1)],bbox_params=bbox_params),
        
        Compose(transforms=[OneOf([
            Blur(blur_limit=5, p=1),
            MotionBlur(blur_limit=5, p=1),
            MedianBlur(blur_limit=5, p=1),],
            p=1)],bbox_params=bbox_params),
        
        Compose(transforms=[OneOf([
            ChannelDropout(p=1.0, channel_drop_range=(1, 1), fill_value=0),
            ChannelShuffle(always_apply=False, p=1.0),
            RGBShift(p=1.0, r_shift_limit=(-40,40), g_shift_limit=(-40,40), b_shift_limit=(-40,40))
            ],p=1)],bbox_params=bbox_params),

        Compose(transforms=[
            Flip(p=1)],
            bbox_params=bbox_params),
        
        Compose(transforms=[
            RandomResizedCrop(p=1,height=1080,width=1920,scale=(0.6,0.9),ratio=(0.75,4))],
            bbox_params=bbox_params),
        
        Compose(transforms=[
            Rotate(p=1, limit=(-40, 40), interpolation=0, border_mode=0, value=(0, 0, 0))],
            bbox_params=bbox_params),
        
        Compose(transforms=[
            ShiftScaleRotate(p=1, shift_limit=(-0.05, 0.05), scale_limit=(-0.5, 0.5), rotate_limit=(-20, 20))],
            bbox_params=bbox_params),
        
        Compose(transforms=[
            ShiftScaleRotate(p=1, shift_limit=(-0.25, 0.25), scale_limit=(-0.1, 0.1), rotate_limit=(-20, 20))],
            bbox_params=bbox_params)
        ]

    return aug


def main():

    # 测试
    img_path = ('/media/lcq/Data/modle_and_code/DataSet/Dataset_Tools/dataset/detection/anno/')         # 要扩增的 jpg 路径
    xml_path = ('/media/lcq/Data/modle_and_code/DataSet/Dataset_Tools/dataset/detection/xml/')          # 要扩增的 xml 路径
    aug_img_path = ('/media/lcq/Data/modle_and_code/DataSet/Dataset_Tools/dataset/detection/aug_anno/') # 扩增后的 jpg 路径
    aug_xml_path = ('/media/lcq/Data/modle_and_code/DataSet/Dataset_Tools/dataset/detection/aug_xml/')  # 扩增后的 xml 路径
    
    # 图像增强数量
    num = 8

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

        # 分别读取
        image = cv2.imread(jpg_path_temp)
        boxes = parse_xml(xml_path_temp)

        # 原图保存到扩增保存路径
        shutil.copy(jpg_path_temp, aug_img_path + "{}.jpg".format(image_name))
        shutil.copy(xml_path_temp, aug_xml_path + "{}.xml".format(image_name))

        for i in range(0,num):
            
            # 每次依次使用所有变换
            # aug = mask_aug()                         
            
            # 每次只使用一种变换
            # 当扩增数量大于方法数量时从头开始
            aug = mask_one_aug()
            if i > len(aug):
                aug = aug[(i%len(aug))]       
            else:
                aug = aug[i]

            augmented = aug(image=image, bboxes=boxes)
            aug_image = augmented['image']
            aug_boxes = augmented['bboxes']

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