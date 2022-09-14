# 修改xml文件中类别的名称
# 参考: https://blog.csdn.net/qq_47733923/article/details/124712118


import os.path
import sys
import time
from tracemalloc import start
import xml.dom.minidom


# xml文件存放路径
xml_path = '/home/xxtc/lichuan/Dataset/baidu783+433/Annotations/'


# 需删除的类名
# delete_name = ['spray_alcohol','metal_can','iron_shoe', 'glass_bottle','umbrella',
#               'nail_clippers','metal_cup','scissor', 'drink_bottle']
# 需替换的类名 {'原始类别名称': '新名称'}
# replace_name = {'Lighter'        : 'lighter',
#                'Pressure_vessel': 'pressure_tank',
#                'Battery'        : 'battery'}

# 测试数据
# xml_path = 'dataset/xml/'
# delete_name = ['dog']
# replace_name = {'TRAIN': 'Train'}

delete_name = []
replace_name = { 'smoking': 'smoke'}

# 修改后的文件是否单独保存
is_copy = False
xml_path_new = None

# 文件名列表
files = os.listdir(xml_path)
file_num = len(files)
print('共读取 {} 个文件'.format(file_num))

start_time = time.time()

for i, xmlFile in enumerate(files):

    print('{}/{}: {} ...'.format(i+1, file_num, xmlFile))

    dom = xml.dom.minidom.parse(xml_path + '/' + xmlFile)
    root = dom.documentElement

    objects = root.getElementsByTagName('object')

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

    # 确定保存路径
    if is_copy:
        xml_name = xml_path_new + '/' + xmlFile
    else:
        xml_name = xml_path + '/' + xmlFile

    # 保存修改后的xml文件
    with open(xml_name, 'w') as fh:
        dom.writexml(fh)

print('OVER, 用时：{}'.format(time.time() - start_time))
