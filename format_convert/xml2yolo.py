#==============================================
# 将 labelImg 得到的 xml 数据转化为 YOLO 所用的 TXT 数据
# lichuan
# lc@dlc618.com
# 2021.7.20
#==============================================

import time
import cv2
import os
import xml.etree.ElementTree as ET


def xml_txt(txt_path,     
			image_path, 
			path, 
			labels):
	
	cnt = 1
	# 遍历图片文件夹
	for (root, dirname, files) in os.walk(image_path):
		
		img_num = len(files)
		# 获取图片名
		for ft in files:

			print('{}/{}:{} in processing...'.format(cnt, img_num, ft))

			# ft是图片名字+扩展名，替换txt,xml格式
			ftxt = ft.replace(ft.split('.')[1], 'txt')
			fxml = ft.replace(ft.split('.')[1], 'xml')
			
			# xml文件路径
			xml_path = os.path.join(path, fxml)
			# txt文件路径
			ftxt_path = os.path.join(txt_path, ftxt)

			# 解析xml
			tree = ET.parse(xml_path)
			root = tree.getroot()
			
			# 获取weight,height
			size = root.find('size')
			w = size.find('width').text
			h = size.find('height').text
			dw = 1/int(w)
			dh = 1/int(h)
			
			# 初始化line
			line = ''
			for item in root.findall('object'):
				# 提取label,并获取索引
				label_name = item.find('name').text

				# 根据目标类型确定目标索引，当不存在跳过
				try:
					label = labels.index(label_name)
				
					# 提取信息labels, x, y, w, h 
					# 多框转化
					for box in item.findall('bndbox'):
						xmin = float(box.find('xmin').text)
						ymin = float(box.find('ymin').text)
						xmax = float(box.find('xmax').text)
						ymax = float(box.find('ymax').text)

						# x, y, w, h 归一化
						center_x = ((xmin + xmax) / 2) * dw
						center_y = ((ymin + ymax) / 2) * dh
						bbox_width = (xmax-xmin) * dw
						bbox_height = (ymax-ymin) * dh
						
						print('  From:',label_name,xmin,ymin,xmax,ymax)
						print('  To  :',label,center_x,center_y,bbox_width,bbox_height)
						
						# 传入信息，txt是字符串形式 - Win
						line += '{} {} {} {} {}'.format(label,center_x,center_y,bbox_width,bbox_height) + '\n'              
						# 传入信息，txt是字符串形式 - Linux
						# line += '{} {} {} {} {}'.format(label,center_x,center_y,bbox_width,bbox_height) + '/n'              
				
				except ValueError:
						print('  From: {} {} {} {} {} {}  To: Skiped',label_name,xmin,ymin,xmax,ymax)

			# 将txt信息写入文件
			with open(ftxt_path, 'w') as f_txt:
				f_txt.write(line)
			cnt += 1

if __name__ == '__main__':

	# 存放图片的文件目录
	image_path = 'D:/Code/DATASET/RailSample/images'
	# 存放xml的文件目录
	xml_path = 'D:/Code/DATASET/RailSample/xmls'
	# yolo存放生成txt的文件目录
	txt_path = 'D:/Code/DATASET/RailSample/txts_2'

	# 测试
	# image_path = 'dataset/jpgs'
	# xml_path = 'dataset/xml'
	# txt_path = 'dataset/txt'
	# labels = ['person', 'train']

	# 标签
	
	labels_railsample_2 = ['person', 'train']
	
	labels_railsample = ['person', 'bicycle', 'car', 'motorbike', 'tricycle', 'train', 'truck',
				   'forklift', 'bus', 'bag', 'dog', 'box', 'stone', 'light']

	labels_icig = [ 'pinA_normal', 'screw_normal', 'pinB_miss',
					'puller_normal', 'pinB_normal', 'pinD_latent',
					'pinD_normal', 'puller_miss', 'pinC_normal',
					'nut', 'screw_miss', 'pinA_miss',
					'pinD_miss', 'nut_normal', 'pinA_latent',
					'pinB_latent', 'pinC_miss', 'pinC_latent' ]

	xml_txt(txt_path, image_path, xml_path, labels_railsample_2)

	print('Over')
	time.sleep(50)