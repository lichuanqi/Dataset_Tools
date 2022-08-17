#==========================================================
# 功能：
# 		将原始数据集按照一定的比例分割成 train:valid:test
#		分割好的数据复制到指定的文件夹
#		根据文件名和路径生成图片列表 train.txt
# LICHUAN，lc@dlc618.com
# 参考：https://www.freesion.com/article/4723305868/
#==========================================================


import os
import sys
import random

import shutil
import time
from tqdm import tqdm


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
		image_path = path + '/' + image + '\n'
		# Linux
		# image_path = os.path.join(jpgs_path,image,'/n')

		with open(txt_name, 'a') as t_txt:
			t_txt.write(image_path)

	return True
		

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
jpgs_path = 'D:/CodePost/Xray_select/jpgs/'
masks_path = 'D:/CodePost/Xray_select/xmls/'

save_path = 'D:/CodePost/Xray_select/'
pre_path = ''
train_txt_name = os.path.join(save_path, 'train.txt')           # train.txt
val_txt_name = os.path.join(save_path, 'val.txt')
test_txt_name = os.path.join(save_path, 'test.txt')

train_image_path = os.path.join(save_path, 'train/images')      # 训练图片
train_label_path = os.path.join(save_path, 'train/labels')      # 训练标注
val_image_path   = os.path.join(save_path, 'val/images')
val_label_path   = os.path.join(save_path, 'val/labels')
test_image_path  = os.path.join(save_path, 'test/images')
test_label_path  = os.path.join(save_path, 'test/labels')

# 保存路径 - 自定义
# save_path = '/media/lcq/Data/modle_and_code/DataSet/RailGuard/train'
# train_image_path = os.path.join(save_path, 'train_image')
# train_label_path = os.path.join(save_path, 'train_label')
# val_image_path   = os.path.join(save_path, 'val_image')
# val_label_path   = os.path.join(save_path, 'val_label')
# test_image_path  = os.path.join(save_path, 'test_image')
# test_label_path  = os.path.join(save_path, 'test_label')

# 保存路径 - YOLO V5训练用
# save_path = 'D:/Code/DATASET/RailSample'
# train_txt_name = os.path.join(save_path, 'train.txt')           # train.txt
# val_txt_name = os.path.join(save_path, 'val.txt')
# test_txt_name = os.path.join(save_path, 'test.txt')
# train_image_path = os.path.join(save_path, 'train/images')      # 训练图片
# train_label_path = os.path.join(save_path, 'train/labels')      # 训练标注
# val_image_path   = os.path.join(save_path, 'val/images')
# val_label_path   = os.path.join(save_path, 'val/labels')
# test_image_path  = os.path.join(save_path, 'test/images')
# test_label_path  = os.path.join(save_path, 'test/labels')

# 划分比例
train, val, test = 0.7, 0.2, 0.1

# 保存参数
is_copy = True        # 将分割好的数据集全部图片和标注复制到指定路径下
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

	txt_write(pre_path + 'train/images', train_list, train_txt_name)
	txt_write(pre_path + 'val/images'  , valid_list,val_txt_name)
	txt_write(pre_path + 'test/images' , test_list,test_txt_name)

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
		# shutil.copy(os.path.join(masks_path,name+'.png'), 
		# 			os.path.join(train_label_path,name+'.png'))
	
	for image in tqdm(valid_list,desc='Val List'):
		name = image.split('.')[0]
		shutil.copy(os.path.join(jpgs_path,image), 
					os.path.join(val_image_path,image))
		# shutil.copy(os.path.join(masks_path,name+'.png'), 
		# 			os.path.join(val_label_path,name+'.png'))

	for image in tqdm(test_list,desc='Test List'):
		name = image.split('.')[0]
		shutil.copy(os.path.join(jpgs_path,image), 
					os.path.join(test_image_path,image))
		# shutil.copy(os.path.join(masks_path,name+'.png'), 
		# 			os.path.join(test_label_path,name+'.png'))

	print('====================== Copy End ======================')