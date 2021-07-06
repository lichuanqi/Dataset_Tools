#!/usr/bin/python
# -*- coding: UTF-8 -*-

#==============================================
# 将labelme得到的json数据转化为训练所用的uint8数据
# lichuan
# lc@dlc618.com
# 2021.6.17
#==============================================


import argparse
import json
import os
import os.path as osp
import base64
import warnings
from tqdm import tqdm
 
import PIL.Image
import yaml
 
from labelme import utils
 
import cv2
import numpy as np
from skimage import img_as_ubyte
 
from sys import argv
 
def main():
    print("This script is aimed to demonstrate how to convert the\n"
          "JSON file to a single image dataset, and not to handle\n"
          "multiple JSON files to generate a real-use dataset.")
 
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_file', type=str, \
						# default='/media/lcq/Data/modle_and_code/DataSet/Segmentation_Dataset_Tools/dataset/jsons',
                        default='/media/lcq/Data/modle_and_code/DataSet/RailGuard200/jsons',
                        help='JSON Path')
    parser.add_argument('--out_masks', type=str, \
					 	# default='/media/lcq/Data/modle_and_code/DataSet/Segmentation_Dataset_Tools/dataset/masks',
                        default='/media/lcq/Data/modle_and_code/DataSet/RailGuard200/masks',
                        help='masks save path')
    parser.add_argument('--out_vizs', type=str, \
					 	# default='/media/lcq/Data/modle_and_code/DataSet/Segmentation_Dataset_Tools/dataset/vizs',
                        default='/media/lcq/Data/modle_and_code/DataSet/RailGuard200/vizs',
                        help='viz save path')
    args = parser.parse_args()
 
    json_file = args.json_file
    mask_path = args.out_masks
    viz_path = args.out_vizs

    #freedom
    list_path = os.listdir(json_file)
    filenum = len(list_path)

    print('================ Start ================')
    print('JSON Path    : {}'.format(json_file))
    print('File Number  : {}'.format(filenum))

    for i in range(0,len(list_path)):
        
        # json 文件绝对路径
        path = os.path.join(json_file,list_path[i])
        
        if os.path.isfile(path):
 
            data = json.load(open(path))
            img = utils.img_b64_to_arr(data['imageData'])
            lbl, lbl_names = utils.labelme_shapes_to_label(img.shape, data['shapes'])

            captions = ['%d: %s' % (l, name) for l, name in enumerate(lbl_names)]
            
            save_file_name = osp.basename(path).split('.')[0]

            # 标注结果可视化
            lbl_viz = utils.draw_label(lbl, img, captions)
 
            # if not osp.exists(json_file + '/' + 'labelme_json'):
                # os.mkdir(json_file + '/' + 'labelme_json')
            # labelme_json = json_file + '/' + 'labelme_json'
 			
			# 为每个图像新建一个同名的文件夹
            # out_dir1 = labelme_json + '/' + save_file_name
            # if not osp.exists(out_dir1):
                # os.mkdir(out_dir1)
            # 将原始图片、标签、标签可视化的结果都保存在同名文件夹内
            # PIL.Image.fromarray(img).save(out_dir1+'/'+save_file_name+'_img.png')
            # PIL.Image.fromarray(lbl).save(out_dir1+'/'+save_file_name+'_label.png')
            # PIL.Image.fromarray(lbl_viz).save(out_dir1+'/'+save_file_name+'_label_viz.png')
    
			# mask文件保存到 --out_masks
            if not osp.exists(mask_path):
                os.mkdir(mask_path)

            # viz文件保存到 --out_vizs            
            if not osp.exists(viz_path):
                os.mkdir(viz_path)
			
            mask_dst = img_as_ubyte(lbl) 
            cv2.imwrite(mask_path+'/'+save_file_name+'.png',mask_dst)

            viz_dst = img_as_ubyte(lbl_viz)
            cv2.imwrite(viz_path+'/'+save_file_name+'.png',viz_dst)

            # TXT YAML 文件保存
            # with open(osp.join(out_dir1, 'label_names.txt'), 'w') as f:
            #     for lbl_name in lbl_names:
            #         f.write(lbl_name + '\n')
 
            # info = dict(label_names=lbl_names)
            # with open(osp.join(out_dir1, 'info.yaml'), 'w') as f:
            #     yaml.safe_dump(info, f, default_flow_style=False)
 
            print('{}/{}: {} result Saved'.format(i+1,filenum,list_path[i]))
 
if __name__ == '__main__':
    #base64path = argv[1]
    main()