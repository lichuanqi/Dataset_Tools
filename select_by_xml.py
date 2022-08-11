# 根据xml数据挑选包含指定类别的图片数据，并按照一定格式重命名。

import os
import shutil
import xml.etree.ElementTree as ET
import xml.dom.minidom


jpgs_path = 'D:/CodePost/PIXray_300examples/jpgs/'
json_path = 'D:/CodePost/PIXray_300examples/jsons/'
xmls_path = 'D:/CodePost/PIXray_300examples/xmls/'

class_select = ['Lighter','Pressure_vessel','Battery','Gun','Fireworks']

is_copy = True
path_new = 'D:/CodePost/Xray_all/'
jpgs_path_new = path_new + 'jpgs/'
json_path_new = path_new + 'jsons/'
xmls_path_new = path_new + 'xmls/'

is_rename = True
name_pre = 'PIXray_'

def selete_xml_file(xmls_path):

    name_select = []     # 符合条件的文件名
    for xmlFile in os.listdir(xmls_path):

        dom = xml.dom.minidom.parse(os.path.join(xmls_path, xmlFile))
        root = dom.documentElement
        name = root.getElementsByTagName('name')
        
        for i in range(len(name)):
            if name[i].firstChild.data in class_select and xmlFile not in name_select:
                name_select.append(xmlFile)
                continue

    return name_select


def copy_file(name_select):

    if not os.path.exists(jpgs_path_new):
        os.mkdir(jpgs_path_new)
    if not os.path.exists(xmls_path_new):
        os.mkdir(xmls_path_new)
    if not os.path.exists(json_path_new):
        os.mkdir(json_path_new)

    for name in name_select:
        file_name = name.split('.')[0]

        jpgFile = jpgs_path + file_name + '.jpg'
        jsonFile = json_path + file_name + '.json'
        xmlFile = xmls_path + file_name + '.xml'

        if is_rename:
            file_name = name_pre + file_name
        
        jpgFile_new = jpgs_path_new + file_name + '.jpg'
        xmlFile_new  = xmls_path_new + file_name + '.xml'
        jsonFile_new = json_path_new + file_name + '.json'


        shutil.copyfile(jpgFile, jpgFile_new)
        shutil.copyfile(xmlFile, xmlFile_new)
        shutil.copyfile(jsonFile, jsonFile_new)


if __name__ == '__main__':

    name_select = selete_xml_file(xmls_path)
    print('共选取 {} 条数据。'.format(len(name_select)))

    if is_copy:
        copy_file(name_select)