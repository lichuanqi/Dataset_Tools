import argparse
import base64
import json
import os
import os.path as osp

import imgviz
import PIL.Image
import cv2

from labelme.logger import logger
from labelme import utils


def main():
    logger.warning(
        "This script is aimed to demonstrate how to convert the "
        "JSON file to a single image dataset."
    )
    logger.warning(
        "It won't handle multiple JSON files to generate a "
        "real-use dataset."
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--images", default='C:/Users/1/Desktop/6165expresssheet/300-399png-labeled/')
    parser.add_argument("-j", "--jsons", default='C:/Users/1/Desktop/6165expresssheet/jsons')
    parser.add_argument("-o", "--out"  , default='C:/Users/1/Desktop/6165expresssheet/')
    args = parser.parse_args()

    json_file = args.jsons
    save_path = args.out

    save_path_masks = os.path.join(save_path, 'masks')
    save_path_vizs = os.path.join(save_path, 'vizs')

    # 保存路径不存在就新建文件夹    
    if not os.path.exists(save_path_masks):
        os.makedirs(save_path_masks)
    if not os.path.exists(save_path_vizs):
        os.makedirs(save_path_vizs)

    filelist = os.listdir(json_file)
    filenum = len(filelist)

    print('================ Start ================')
    print('JSON Path    : {}'.format(json_file))
    print('JSON Path    : {}'.format(filelist))
    print('File Number  : {}'.format(filenum))
    
    # 保存所有类别及id
    labels_all = {}

    # 遍历文件列表
    for i in range(0, len(filelist)): 

        # 文件路径
        path = os.path.join(json_file, filelist[i])
        # 文件名
        image_name = filelist[i].split('.')[0]

        if os.path.isdir(path):  #如果是目录则读取下一个
            continue

        data = json.load(open(path))   # 读取目录标注文件
        imageData = data.get("imageData")

        if not imageData:
            imagePath = os.path.join(os.path.dirname(json_file), data["imagePath"])
            with open(imagePath, "rb") as f:
                imageData = f.read()
                imageData = base64.b64encode(imageData).decode("utf-8")
        img = utils.img_b64_to_arr(imageData)

        label_name_to_value = {"_background_": 0}
        for shape in sorted(data["shapes"], key=lambda x: x["label"]):
            label_name = shape["label"]

            if label_name in label_name_to_value:
                label_value = label_name_to_value[label_name]
            else:
                label_value = len(label_name_to_value)
                label_name_to_value[label_name] = label_value

        # 保存类别列表
        for key, value in label_name_to_value.items():
            if key not in labels_all.keys():
                labels_all[key] = value

        # 标注文件
        lbl, _ = utils.shapes_to_label(img.shape, data["shapes"], label_name_to_value)

        label_names = [None] * (max(label_name_to_value.values()) + 1)
        for name, value in label_name_to_value.items():
            label_names[value] = name

        # 标注可视化文件
        lbl_viz = imgviz.label2rgb(lbl, imgviz.asgray(img), label_names=label_names, loc="rb")

        # 保存名称
        save_name_mask = os.path.join(save_path_masks, image_name + '.png')
        save_path_viz = os.path.join(save_path_vizs, image_name + '.png')
        
        cv2.imwrite(save_name_mask, lbl)
        cv2.imwrite(save_path_viz, lbl_viz)

        logger.info("Mask is saved to: {}".format(save_name_mask))

    save_path_label_list = os.path.join(save_path, 'label_list.txt')
    with open(save_path_label_list, "w") as f:
        for key, value in label_name_to_value.items():
            f.write('{}: {}\n'.format(key, value))

    print('OVER')
    print(labels_all)


if __name__ == "__main__":
    main()
