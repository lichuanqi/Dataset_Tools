# 修改xml文件中类别的名称
# 参考: https://blog.csdn.net/qq_47733923/article/details/124712118

from dataclasses import replace
import os.path
import sys
import xml.dom.minidom


# xml文件存放路径
# xml_path = 'C:/Users/soli/Desktop/1'
# 需删除的类名
# delete_name = ['spray_alcohol']
# 需替换的类名 {'原始类别名称': '新名称'}
# replace_name = {'Lighter'        : 'lighter',
#                 'Pressure_vessel': 'pressure_tank',
#                 'Battery'        : 'battery'}

# 测试数据
xml_path = 'dataset/xml/'
delete_name = ['dog']
replace_name = {'TRAIN': 'Train'}

# 文件名列表
files = os.listdir(xml_path)
file_num = len(files)
print('共读取 {} 个文件'.format(file_num))

for i, xmlFile in enumerate(files):

    print('{}/{}: {} ...'.format(i+1, file_num, xmlFile))

    dom = xml.dom.minidom.parse(xml_path + '/' + xmlFile)
    root = dom.documentElement

    objects = root.getElementsByTagName('object')
    newfilename = root.getElementsByTagName('name')

    for i, obj in enumerate(objects):
        class_name = obj.getElementsByTagName('name')[0].firstChild.data

        # 先判断删除
        if class_name in delete_name:
            root.removeChild(obj)
            print('-- 删除: {}'.format(class_name))

        # 再判断替换
        if class_name in replace_name.keys():
            obj.getElementsByTagName('name')[0].firstChild.data = replace_name[class_name]
            print('-- 替换: {} -> {}'.format(class_name, replace_name[class_name]))
        

    # for i, t in enumerate(newfilename):
    #     class_name = t.firstChild.data
        
    #     # 后判断替换
    #     if class_name in replace_name.keys():
    #         newfilename[i].firstChild.data = replace_name[class_name]
    #         print('-- 替换: {} -> {}'.format(class_name, replace_name[class_name]))

    with open(os.path.join(xml_path, xmlFile), 'w') as fh:
        dom.writexml(fh)
