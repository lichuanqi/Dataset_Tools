# coding:utf-8
# 将COCO数据集的 JSON 文件转换为VOC的 xml 文件


import os
import json
import cv2
from lxml import etree
import xml.etree.cElementTree as ET
import time


coco_dict = {1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus', 7: 'train', 8: 'truck',
             9: 'boat', 10: 'traffic light', 11: 'fire hydrant', 13: 'stop sign', 14: 'parking meter', 15: 'bench',
             16: 'bird', 17: 'cat', 18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear', 24: 'zebra',
             25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag', 32: 'tie', 33: 'suitcase', 34: 'frisbee',
             35: 'skis', 36: 'snowboard', 37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
             41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle', 46: 'wine glass', 47: 'cup',
             48: 'fork', 49: 'knife', 50: 'spoon', 51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
             56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut', 61: 'cake', 62: 'chair', 63: 'couch',
             64: 'potted plant', 65: 'bed', 67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
             75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven', 80: 'toaster', 81: 'sink',
             82: 'refrigerator', 84: 'book', 85: 'clock', 86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier',
             90: 'toothbrush'}

coco_names = [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
               'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
               'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
               'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
               'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
               'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
               'hair drier', 'toothbrush' ] 

voc_names  = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle',
              'bus', 'car', 'cat', 'chair', 'cow', 'diningtable',
              'dog', 'horse', 'motorbike', 'pottedplant',
              'sheep', 'sofa', 'train', 'tvmonitor', 'person']


id_list = [1,7]
names_list = ['person', 'train',]

COCO_images = 'D:/Code/DATASET/5151/validation/data/'
Json_addr = "D:/Code/DATASET/5151/validation/labels.json"

im_ext = 'jpg'
im_num = 0
ob_count = 0
im_pairs = dict()

# 设置保存路径
xml_dir = 'D:/Code/DATASET/5151/validation/xml/'
im_dir = 'D:/Code/DATASET/5151/validation/images'

# 保存路径不存在就新建
if not os.path.isdir(xml_dir):
    os.mkdir(xml_dir)
if not os.path.isdir(im_dir):
    os.mkdir(im_dir)

print('Reading JSON ...')

with open(Json_addr) as json_data:
    annotation_list = json.load(json_data)

start_time = time.time()
print('--- Start Operation ---', start_time)

for i in range(0, len(annotation_list["annotations"])):
    category_id = annotation_list["annotations"][i]["category_id"]

    if category_id in id_list:
        # print('HIT -->', im_num)
        cat_name = names_list[id_list.index(category_id)]
        im_id = (str(annotation_list["annotations"][i]["image_id"]))
        xmin = int(annotation_list["annotations"][i]["bbox"][0])
        ymin = int(annotation_list["annotations"][i]["bbox"][1])
        xmax = int(xmin+annotation_list["annotations"][i]["bbox"][2])
        ymax = int(ymin+annotation_list["annotations"][i]["bbox"][3])

        z = '0'
        for sf in range((len(im_id)), 11):   # imname 12 basamaklı olması için
            z = z + "0"
        im_name = z + im_id

        if os.path.exists(os.path.join(im_dir, str(im_pairs.get(im_name, 'None')) + '.' + im_ext)):
            # ---add object to imnum.xml---

            # read the xml root
            tree = ET.parse(os.path.join(xml_dir, str(im_pairs[im_name]) + '.xml'))
            root = tree.getroot()

            # Convert root to etree

            xml_str = ET.tostring(root)
            troot = etree.fromstring(xml_str)  # etree object

            # create new object element
            ob = etree.Element('object')
            etree.SubElement(ob, 'name').text = cat_name
            etree.SubElement(ob, 'pose').text = 'Unspecified'
            etree.SubElement(ob, 'truncated').text = '0'
            etree.SubElement(ob, 'difficult').text = '0'

            bbox = etree.SubElement(ob, 'bndbox')
            etree.SubElement(bbox, 'xmin').text = str(xmin)
            etree.SubElement(bbox, 'ymin').text = str(ymin)
            etree.SubElement(bbox, 'xmax').text = str(xmax)
            etree.SubElement(bbox, 'ymax').text = str(ymax)

            # prettify the object
            xml_str = etree.tostring(ob, pretty_print=True)
            ob_pretty = etree.fromstring(xml_str)

            # append etree object to etree root(troot)
            troot.append(ob_pretty)

            # overwrite the old xml
            xml_str = etree.tostring(troot, pretty_print=True)

            with open(os.path.join(xml_dir, str(im_pairs[im_name]) + '.xml'), 'wb') as output:
                output.write(xml_str)

            print('--- Added {} to '.format(cat_name), str(im_pairs[im_name]) + '.xml' ' ---')

        else:

            # Copy image as im_num.jpg
            with open(os.path.join(COCO_images, im_name + '.' + im_ext), 'rb') as rf:
                with open(os.path.join(im_dir, str(im_num) + '.' + im_ext), 'wb') as wf:
                    for line in rf:
                        wf.write(line)
            # make imnum.xml

            # -get imsize(widht, height, depth)

            # Resimlerin olduğu klasör
            im_cv2 = cv2.imread(os.path.join(COCO_images, im_name + '.' + im_ext))
            height, width, depth = im_cv2.shape

            # Form the file
            annotation = ET.Element('annotation')
            ET.SubElement(annotation, 'folder').text = im_dir
            ET.SubElement(annotation, 'filename').text = str(im_num) + '.' + im_ext
            ET.SubElement(annotation, 'segmented').text = '0'
            size = ET.SubElement(annotation, 'size')
            ET.SubElement(size, 'width').text = str(width)
            ET.SubElement(size, 'height').text = str(height)
            ET.SubElement(size, 'depth').text = str(depth)

            ob = ET.SubElement(annotation, 'object')
            ET.SubElement(ob, 'name').text = cat_name
            ET.SubElement(ob, 'pose').text = 'Unspecified'
            ET.SubElement(ob, 'truncated').text = '0'
            ET.SubElement(ob, 'difficult').text = '0'

            bbox = ET.SubElement(ob, 'bndbox')
            ET.SubElement(bbox, 'xmin').text = str(xmin)
            ET.SubElement(bbox, 'ymin').text = str(ymin)
            ET.SubElement(bbox, 'xmax').text = str(xmax)
            ET.SubElement(bbox, 'ymax').text = str(ymax)

            # Save the file
            xml_str = ET.tostring(annotation)
            root = etree.fromstring(xml_str)
            xml_str = etree.tostring(root, pretty_print=True)  # Entire content of the xml

            save_path = os.path.join(xml_dir, str(im_num) + '.' + 'xml')  # Create save path with imnum.xml

            with open(save_path, 'wb') as temp_xml:
                temp_xml.write(xml_str)
            # keep record of which xml is paired with which image from coco_Set
            im_pairs[im_name] = im_num

            print('Copied imfile--> {} --- Object count--> {}'.format(str(im_num) + '.' + im_ext, ob_count))

            im_num += 1
        ob_count += 1

print('Finished with {} objects in {} images in {} seconds'.format(ob_count, im_num, time.time() - start_time))