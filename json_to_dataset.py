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
    warnings.warn("This script is aimed to demonstrate how to convert the\n"
                  "JSON file to a single image dataset, and not to handle\n"
                  "multiple JSON files to generate a real-use dataset.")
 
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_file', type=str, \
						default='/media/lcq/Data/modle_and_code/DataSet/DatasetTools/dataset/json_test')
    parser.add_argument('--out', type=str, \
					 	default='/media/lcq/Data/modle_and_code/DataSet/DatasetTools/dataset/masks_test')
    args = parser.parse_args()
 
    json_file = args.json_file
    mask_path = args.out

    #freedom
    list_path = os.listdir(json_file)
    print('freedom =', json_file)
    for i in tqdm(range(0,len(list_path))):
        path = os.path.join(json_file,list_path[i])
        if os.path.isfile(path):
 
            data = json.load(open(path))
            img = utils.img_b64_to_arr(data['imageData'])
            lbl, lbl_names = utils.labelme_shapes_to_label(img.shape, data['shapes'])
            # lbl, lbl_names = utils.shapes_to_label(img.shape, data['shapes'])

            captions = ['%d: %s' % (l, name) for l, name in enumerate(lbl_names)]
            
            # 标注结果可视化
            lbl_viz = utils.draw_label(lbl, img, captions)

            out_dir = osp.basename(path).split('.')[0]
            save_file_name = out_dir
            out_dir = osp.join(osp.dirname(path), out_dir)
 
            if not osp.exists(json_file + '/' + 'labelme_json'):
                os.mkdir(json_file + '/' + 'labelme_json')
            labelme_json = json_file + '/' + 'labelme_json'
 			
			# 为每个图像新建一个同名的文件夹
            out_dir1 = labelme_json + '/' + save_file_name
            if not osp.exists(out_dir1):
                os.mkdir(out_dir1)
 
            PIL.Image.fromarray(img).save(out_dir1+'/'+save_file_name+'_img.png')
            PIL.Image.fromarray(lbl).save(out_dir1+'/'+save_file_name+'_label.png')
            PIL.Image.fromarray(lbl_viz).save(out_dir1+'/'+save_file_name+'_label_viz.png')
 			
			# 将mask文件储存在 --output 文件夹下，没有的话新建一个
            if not osp.exists(mask_path):
                os.mkdir(mask_path)
			
            mask_pic = cv2.imread(out_dir1+'/'+save_file_name+'_label.png',)
            mask_dst = img_as_ubyte(lbl) 
            print('pic2_deep:',mask_dst.dtype)
            cv2.imwrite(mask_path+'/'+save_file_name+'.png',mask_dst)
 
            with open(osp.join(out_dir1, 'label_names.txt'), 'w') as f:
                for lbl_name in lbl_names:
                    f.write(lbl_name + '\n')
 
            warnings.warn('info.yaml is being replaced by label_names.txt')
            info = dict(label_names=lbl_names)
            with open(osp.join(out_dir1, 'info.yaml'), 'w') as f:
                yaml.safe_dump(info, f, default_flow_style=False)
 
            print('Saved to: %s' % out_dir1)
 
if __name__ == '__main__':
    #base64path = argv[1]
    main()