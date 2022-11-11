#==========================================================
# 功能：
# 		将原始数据集按照一定的比例分割成 train:valid:test
#		分割好的数据复制到指定的文件夹
#		根据文件名和路径生成图片列表 train.txt
# LICHUAN，lc@dlc618.com
# 参考：https://www.freesion.com/article/4723305868/
#==========================================================


import os
import os.path as osp
import sys
import random

import shutil
import time
from tqdm import tqdm
from loguru import	logger

import xml.etree.ElementTree as ET


def mk_if_not_exists(path):
    """
    保存路径不存在时新建
    """
    if not os.path.exists(path):
        os.makedirs(path)

    return True


def txt_write(path, images_list, txt_name):

    for image in images_list:

        # Win
        image_path = path + image + '\n'
        # Linux
        # image_path = os.path.join(jpgs_path,image,'/n')

        with open(txt_name, 'a') as t_txt:
            t_txt.write(image_path)

    return True


def is_pic(img_name):
    valid_suffix = ['JPEG', 'jpeg', 'JPG', 'jpg', 'BMP', 'bmp', 'PNG', 'png']
    suffix = img_name.split('.')[-1]
    if suffix not in valid_suffix:
        return False
    return True


def list_files(dirname):
    """ 列出目录下所有文件（包括所属的一级子目录下文件）
    Args:
        dirname: 目录路径
    """

    def filter_file(f):
        if f.startswith('.'):
            return True
        return False

    all_files = list()
    dirs = list()
    for f in os.listdir(dirname):
        if filter_file(f):
            continue
        if osp.isdir(osp.join(dirname, f)):
            dirs.append(f)
        else:
            all_files.append(f)
    for d in dirs:
        for f in os.listdir(osp.join(dirname, d)):
            if filter_file(f):
                continue
            if osp.isdir(osp.join(dirname, d, f)):
                continue
            all_files.append(osp.join(d, f))
    return all_files


def replace_ext(filename, new_ext):
    """ 替换文件后缀
    Args:
        filename: 文件路径
        new_ext: 需要替换的新的后缀
    """
    items = filename.split(".")
    items[-1] = new_ext
    new_filename = ".".join(items)
    return new_filename


def split_xml2paddle(dataset_dir, val_percent, test_percent, save_dir):
    """
    将labelImg标注的xmls格式的数据集按照比例分为训练集、验证集、测试集,
    用于PaddleDetection的训练
    Args
        dataset_dir	 	: 数据路径,路径下应该有images和xmls文件夹
    """
    all_image_files = list_files(osp.join(dataset_dir, "images"))

    image_anno_list = list()
    label_list = list()
    for image_file in all_image_files:
        if not is_pic(image_file):
            continue
        anno_name = replace_ext(image_file, "xml")
        nano_file = osp.join(dataset_dir, "xmls", anno_name)

        logger.debug(f'image_file: {image_file}, anno_name: {anno_name}')

        if osp.exists(nano_file):
            image_anno_list.append([image_file, anno_name])
            try:
                tree = ET.parse(nano_file)
            except:
                raise Exception("文件{}不是一个良构的xml文件，请检查标注文件".format(nano_file))
            objs = tree.findall("object")
            for i, obj in enumerate(objs):
                cname = obj.find('name').text
                if not cname in label_list:
                    label_list.append(cname)
        else:
            logger.error("The annotation file {} doesn't exist!".format(
                anno_name))

    random.shuffle(image_anno_list)
    image_num = len(image_anno_list)
    val_num = int(image_num * val_percent)
    test_num = int(image_num * test_percent)
    train_num = image_num - val_num - test_num

    train_image_anno_list = image_anno_list[:train_num]
    val_image_anno_list = image_anno_list[train_num:train_num + val_num]
    test_image_anno_list = image_anno_list[train_num + val_num:]

    with open(
            osp.join(save_dir, 'train_list.txt'), mode='w',
            encoding='utf-8') as f:
        for x in train_image_anno_list:
            file = osp.join("images", x[0])
            label = osp.join("xmls", x[1])
            f.write('{} {}\n'.format(file, label))
    with open(
            osp.join(save_dir, 'val_list.txt'), mode='w',
            encoding='utf-8') as f:
        for x in val_image_anno_list:
            file = osp.join("images", x[0])
            label = osp.join("xmls", x[1])
            f.write('{} {}\n'.format(file, label))
    if len(test_image_anno_list):
        with open(
                osp.join(save_dir, 'test_list.txt'), mode='w',
                encoding='utf-8') as f:
            for x in test_image_anno_list:
                file = osp.join("images", x[0])
                label = osp.join("xmls", x[1])
                f.write('{} {}\n'.format(file, label))
    with open(
            osp.join(save_dir, 'labels.txt'), mode='w', encoding='utf-8') as f:
        for l in sorted(label_list):
            f.write('{}\n'.format(l))

    logger.info(f'train_num: {train_num}, val_num: {val_num}')

    return True


def split_txt2yolo():


    # 数据集路径 - 测试
    # jpgs_path = 'dataset/jpgs'
    # masks_path = 'dataset/masks'

    # 数据集路径 - RailGuard数据集
    # jpgs_path = 'D:/Code/DATASET/RailSample/images'
    # masks_path = 'D:/Code/DATASET/RailSample/txt'
    # jpgs_path = 'D:/Code/DATASET/RailSample/test/images'
    # masks_path = 'D:/Code/DATASET/RailSample/test/labels'
    # pre_path = '/data/home/u19120834/DATASET/RailSample/images'
    # pre_path = '/media/vv/50B0275AB02745B6/lichuan/dataset/Railsample/images'    # 实验室GPU路径

    # 数据集路径 - Xary
    jpgs_path = '/home/xxtc/lichuan/Dataset/baidu783+433/images/'
    masks_path = '/home/xxtc/lichuan/Dataset/baidu783+433/labels/'

    save_path = '/home/xxtc/lichuan/Dataset/baidu783+433/'
    pre_path = ''
    train_txt_name = os.path.join(save_path, 'train.txt')           # train.txt
    val_txt_name = os.path.join(save_path, 'val.txt')
    test_txt_name = os.path.join(save_path, 'test.txt')

    # 保存路径 - 自定义
    train_image_path = os.path.join(save_path, 'train_image')
    train_label_path = os.path.join(save_path, 'train_label')
    val_image_path   = os.path.join(save_path, 'val_image')
    val_label_path   = os.path.join(save_path, 'val_label')
    test_image_path  = os.path.join(save_path, 'test_image')
    test_label_path  = os.path.join(save_path, 'test_label')

    # 保存路径 - YOLO V5训练用
    # save_path = 'D:/Code/DATASET/RailSample'
    # train_image_path = os.path.join(save_path, 'train/images')      # 训练图片
    # train_label_path = os.path.join(save_path, 'train/labels')      # 训练标注
    # val_image_path   = os.path.join(save_path, 'val/images')
    # val_label_path   = os.path.join(save_path, 'val/labels')
    # test_image_path  = os.path.join(save_path, 'test/images')
    # test_label_path  = os.path.join(save_path, 'test/labels')

    # 划分比例
    train, val, test = 0.75, 0.2, 0.05

    # 保存参数
    is_copy = False        # 将分割好的数据集全部图片和标注复制到指定路径下
    is_txt = True          # 生成 三个txt文件，保存所有图片名称

    images_list = os.listdir(jpgs_path)

    # 计算每个组的图片数量
    num  = len(images_list)
    alpha  = int( num  * train )
    beta   = int( num  * (train+val) )
    gamma  = int( num  * (train+val+test) )

    # 随机排序
    random.shuffle(images_list)
    # 按照顺序排序
    # images_list.sort(key=lambda x:int(x.split('.')[0]))

    train_list = images_list[0:alpha]
    valid_list = images_list[alpha:beta]
    test_list  = images_list[beta:gamma]
    
    # 确认划分数量
    print('====================== info ======================')
    print('Total num : ',num)
    print('Train num: ',len(train_list))
    print('Valid num: ',len(valid_list))
    print('Test num : ',len(test_list))

    # 生成txt路径文件
    if is_txt:

        if pre_path	== '':
            pre_path = jpgs_path

        txt_write(pre_path , train_list, train_txt_name)
        txt_write(pre_path , valid_list, val_txt_name)
        txt_write(pre_path , test_list, test_txt_name)

        print('TXT is saved')

    # 复制到指定路径
    if is_copy:

        # 储存文件夹不存在时新建
        mk_if_not_exists(train_image_path)
        mk_if_not_exists(train_label_path)
        mk_if_not_exists(val_image_path)
        mk_if_not_exists(val_label_path)
        mk_if_not_exists(test_image_path)
        mk_if_not_exists(test_label_path)

        print('====================== Copy Start======================')

        for image in tqdm(train_list,desc='Train List'):
            name = image.split('.')[0]
            shutil.copy(os.path.join(jpgs_path,image), 
                        os.path.join(train_image_path,image))
            shutil.copy(os.path.join(masks_path,name+'.png'), 
                        os.path.join(train_label_path,name+'.png'))
        
        for image in tqdm(valid_list,desc='Val List'):
            name = image.split('.')[0]
            shutil.copy(os.path.join(jpgs_path,image), 
                        os.path.join(val_image_path,image))
            shutil.copy(os.path.join(masks_path,name+'.png'), 
                        os.path.join(val_label_path,name+'.png'))

        for image in tqdm(test_list,desc='Test List'):
            name = image.split('.')[0]
            shutil.copy(os.path.join(jpgs_path,image), 
                        os.path.join(test_image_path,image))
            shutil.copy(os.path.join(masks_path,name+'.png'), 
                        os.path.join(test_label_path,name+'.png'))

        print('====================== Copy End ======================')


if __name__ == '__main__':
    dataset_dir = 'D:/Data/Expressbox/'
    val_percent, test_percent = 0.2, 0
    save_dir = dataset_dir
    split_xml2paddle(dataset_dir, val_percent, test_percent, save_dir)