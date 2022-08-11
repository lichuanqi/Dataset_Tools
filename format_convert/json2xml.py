# 将labelme生成的json数据转换为xml数据


import os
from select import select
import numpy as np
import codecs
import json
from glob import glob
import cv2
import shutil
from sklearn.model_selection import train_test_split


# json文件路径
jpgs_path  = 'D:/CodePost/Xray_all/jpgs/'
jsons_path = 'D:/CodePost/Xray_all/jsons/'

# 指定类别
is_select = True
class_select = ['Lighter','Pressure_vessel','Battery','Gun','Fireworks']

# 文件重命名
is_rename = False
file_name_new = 20220802001   

# 保存路径
save_path = 'D:/CodePost/Xray_all/'
save_path_jpg = save_path + 'jpgs/'
save_path_xml = save_path + 'xmls/'
if not os.path.isdir(save_path_jpg):
    os.mkdir(save_path_jpg)
if not os.path.isdir(save_path_xml):
    os.mkdir(save_path_xml)

# 3.获取待处理文件
jsons_files = glob(jsons_path + "*.json")
# windows路径
jsons_files = [i.replace("\\","/") for i in jsons_files]
num = len(jsons_files)
print('共读取 {} 条数据: '.format(num))

# 4.读取标注信息并写入 xml
for i, json_filename in enumerate(jsons_files):
    
    print('{}/{}: {}'.format(i, num, json_filename))

    file_name = json_filename.split("/")[-1].split(".json")[0]   # 原始不包含扩展名的图片名
    jpg = jpgs_path + file_name + ".JPG"                         # 原始图片路径
    
    # 新的图片名,主要用于去除中文                            
    if is_rename:
        print(file_name, ' -> ', file_name_new)

        xml_save = save_path_xml + str(file_name_new) + ".xml"          # 新的xml文件路径
        jpg_save = save_path_jpg + str(file_name_new) + ".jpg"          # 新的jpg文件路径

        # 原始图片复制到指定目录下
        shutil.copy(jpg, jpg_save)

    else:
        xml_save = save_path_xml + str(file_name) + ".xml"          # xml文件路径
        jpg_save = jpg                                              # jpg文件路径

    json_file = json.load(open(json_filename, "r", encoding="utf-8"))

    jpg = cv2.imread(jpg_save)
    height, width, channels = jpg.shape

    with codecs.open(xml_save, "w", "utf-8") as xml:

        xml.write('<annotation>\n')
        xml.write('\t<folder>' + 'CPST' + '</folder>\n')
        xml.write('\t<filename>' + file_name + ".jpg" + '</filename>\n')
        # xml.write('\t<source>\n')
        # xml.write('\t\t<database>ECM_Data</database>\n')
        # xml.write('\t\t<annotation>ECM</annotation>\n')
        # xml.write('\t\t<image>flickr</image>\n')
        # xml.write('\t\t<flickrid>NULL</flickrid>\n')
        # xml.write('\t</source>\n')
        # xml.write('\t<owner>\n')
        # xml.write('\t\t<flickrid>NULL</flickrid>\n')
        # xml.write('\t\t<name>XT</name>\n')
        # xml.write('\t</owner>\n')
        xml.write('\t<size>\n')
        xml.write('\t\t<width>' + str(width) + '</width>\n')
        xml.write('\t\t<height>' + str(height) + '</height>\n')
        xml.write('\t\t<depth>' + str(channels) + '</depth>\n')
        xml.write('\t</size>\n')
        xml.write('\t\t<segmented>0</segmented>\n')
        for multi in json_file["shapes"]:

            labelName=multi["label"]
            if is_select and labelName in class_select:
                points = np.array(multi["points"])
                xmin = min(points[:, 0])
                xmax = max(points[:, 0])
                ymin = min(points[:, 1])
                ymax = max(points[:, 1])
                label = multi["label"]
                if xmax <= xmin:
                    pass
                elif ymax <= ymin:
                    pass
                else:
                    xml.write('\t<object>\n')
                    xml.write('\t\t<name>' + labelName+ '</name>\n')
                    xml.write('\t\t<pose>Unspecified</pose>\n')
                    # xml.write('\t\t<truncated>1<\truncated>\n')
                    xml.write('\t\t<difficult>0</difficult>\n')
                    xml.write('\t\t<bndbox>\n')
                    xml.write('\t\t\t<xmin>' + str(int(xmin)) + '</xmin>\n')
                    xml.write('\t\t\t<ymin>' + str(int(ymin)) + '</ymin>\n')
                    xml.write('\t\t\t<xmax>' + str(int(xmax)) + '</xmax>\n')
                    xml.write('\t\t\t<ymax>' + str(int(ymax)) + '</ymax>\n')
                    xml.write('\t\t</bndbox>\n')
                    xml.write('\t</object>\n')
                    print('--', xmin, ymin, xmax, ymax, label)
        xml.write('</annotation>')
    
    file_name_new += 1
    


print('OVER')
