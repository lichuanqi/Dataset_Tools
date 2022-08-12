# 根据xml数据挑选包含指定类别的图片数据，并按照一定格式重命名。

import os,sys
import shutil
import xml.etree.ElementTree as ET
import xml.dom.minidom


jpgs_path = 'D:/CodePost/Xray_FSOD/X-ray FSOD/test/images/'
# json_path = 'D:/CodePost/PIXray_300examples/jsons/'
xmls_path = 'D:/CodePost/Xray_FSOD/X-ray FSOD/test/xmls/'

class_select = ['laptop','portable_charger_1', 'battery','pressure_tank','lighter',
                'straight_knife', 'folding_knife', 'multi-tool_knife', 'utility_knife',
                'mobile_phone']

is_copy = False
path_new = 'D:/CodePost/Xray_select/'
jpgs_path_new = path_new + 'jpgs/'
# json_path_new = path_new + 'jsons/'
xmls_path_new = path_new + 'xmls/'

is_rename = False
name_pre = 'FSOD_test_'


def selete_xml_file(xmls_path):

    name_select = []     # 符合条件的文件名
    class_num = {}       # 每个类别的数量

    for xmlFile in os.listdir(xmls_path):

        dom = xml.dom.minidom.parse(os.path.join(xmls_path, xmlFile))
        root = dom.documentElement
        name = root.getElementsByTagName('name')

        for i in range(len(name)):
            
            class_name = name[i].firstChild.data
            # 将包含指定类别名称的文件名暂存到列表
            if class_name in class_select and xmlFile not in name_select:
                name_select.append(xmlFile)

            # 统计每个类别的数量
            if class_name in class_select and class_name not in class_num.keys():
                class_num[class_name] = 1
            elif class_name in class_select and class_name in class_num.keys():
                class_num[class_name] += 1

    return name_select, class_num


def copy_file(name_select):

    if not os.path.exists(jpgs_path_new):
        os.mkdir(jpgs_path_new)
    if not os.path.exists(xmls_path_new):
        os.mkdir(xmls_path_new)
    # if not os.path.exists(json_path_new):
    #     os.mkdir(json_path_new)

    for name in name_select:
        file_name = name.split('.')[0]

        jpgFile = jpgs_path + file_name + '.jpg'
        # jsonFile = json_path + file_name + '.json'
        xmlFile = xmls_path + file_name + '.xml'

        if is_rename:
            file_name = name_pre + file_name
        
        jpgFile_new = jpgs_path_new + file_name + '.jpg'
        xmlFile_new  = xmls_path_new + file_name + '.xml'
        # jsonFile_new = json_path_new + file_name + '.json'


        shutil.copyfile(jpgFile, jpgFile_new)
        shutil.copyfile(xmlFile, xmlFile_new)
        # shutil.copyfile(jsonFile, jsonFile_new)


if __name__ == '__main__':

    name_select, class_num = selete_xml_file(xmls_path)

    print('共选取 {} 条数据。'.format(len(name_select)))
    print('各类别数量：')
    for key,value in class_num.items():
        print('--{: <15}: {}'.format(key, value))

    if is_copy:
        copy_file(name_select)