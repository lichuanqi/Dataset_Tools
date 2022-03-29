#==========================================================
# 功能：
# 		将原始数据集按照一定的比例分割成 train:valid:test
#		分割好的数据复制到指定的文件夹
#		根据文件名和路径生成图片列表 train.txt  （未实现）
# LICHUAN，lc@dlc618.com
# 参考：https://www.freesion.com/article/4723305868/
#==========================================================


import os
import random

import shutil
from tqdm import tqdm

def mk_if_not_exists(path):
	if not os.path.exists(path):
		os.makedirs(path)

	return True
	

# 划分比例
train, val, test = 0.8, 0.15, 0.05

# 数据集路径 - 测试
# jpgs_path = 'dataset/jpgs'
# masks_path = 'dataset/masks'

jpgs_path = '/media/lcq/Data/modle_and_code/DataSet/RailGuard/jpgs'
masks_path = '/media/lcq/Data/modle_and_code/DataSet/RailGuard/masks'

# 保存路径
save_path = '/media/lcq/Data/modle_and_code/DataSet/RailGuard/train'

train_image_path = os.path.join(save_path, 'train_image')
train_label_path = os.path.join(save_path, 'train_label')
val_image_path   = os.path.join(save_path, 'val_image')
val_label_path   = os.path.join(save_path, 'val_label')
test_image_path  = os.path.join(save_path, 'test_image')
test_label_path  = os.path.join(save_path, 'test_label')

# 储存文件夹不存在时新建
mk_if_not_exists(train_image_path)
mk_if_not_exists(train_label_path)
mk_if_not_exists(val_image_path)
mk_if_not_exists(val_label_path)
mk_if_not_exists(test_image_path)
mk_if_not_exists(test_label_path)

images = os.listdir(jpgs_path)

num  = len(images)
alpha  = int( num  * train )
beta   = int( num  * (train+val) )

# 随机排序
random.shuffle(images)
 
train_list = images[0:alpha]
valid_list = images[alpha:beta]
test_list  = images[beta:num]
 
# 确认分割正确
print('====================== info ======================')
print('total num : ',len(test_list)+len(valid_list)+len(train_list))
print('train list: ',len(train_list))
print('valid list: ',len(valid_list))
print('test list : ',len(test_list))

# 复制到指定路径
print('====================== Copy ======================')

for image in tqdm(train_list):
	name = image.split('.')[0]
	shutil.copy(os.path.join(jpgs_path,image), 
				os.path.join(train_image_path,image))
	shutil.copy(os.path.join(masks_path,name+'.png'), 
				os.path.join(train_label_path,name+'.png'))
 
for image in tqdm(valid_list):
	name = image.split('.')[0]
	shutil.copy(os.path.join(jpgs_path,image), 
				os.path.join(val_image_path,image))
	shutil.copy(os.path.join(masks_path,name+'.png'), 
				os.path.join(val_label_path,name+'.png'))

for image in tqdm(test_list):
	name = image.split('.')[0]
	shutil.copy(os.path.join(jpgs_path,image), 
				os.path.join(test_image_path,image))
	shutil.copy(os.path.join(masks_path,name+'.png'), 
				os.path.join(test_label_path,name+'.png'))

print('====================== End ======================')