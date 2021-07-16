#==============================================
# 样本库数据集数据分析
# lichuan
# lc@dlc618.com
# 2021.7.6
#==============================================

import glob,os

import csv
import numpy as np


def get_dir_file(dir_name, pattern = ["*.png","*.jpg","*.jpeg"]):
    '''
    功能
        读取路径下指定后缀的文件路径
    输入
        dir_name ：路径
        pattern  ：文件后缀要求
    输出
        所以符合条件的文件
    '''
    files = []
    for p in pattern:
        for dir,_,_ in os.walk(dir_name):
            files.extend(glob.glob(os.path.join(dir,p)))
    
    return files


def writer_csv(csv_file,data):
    '''
    功能:
        列表数据保存为 csv 文件
    输入:
        csv_file : 保存路径
        data     : 要保存的列表数据
    输出:
        成功
    '''

    with open(csv_file, 'w', newline='') as f: 
        writer = csv.writer(f)
        writer.writerows(data)

    return True


def read_csv(csv_file):
    '''
    功能:
        读取 csv 文件为列表
    输入:
        csv_file : csv 文件路径
    输出:
        data     : 列表数据
    '''
    data = list()

    with open(csv_file, 'r', newline="") as f: 
        reader = csv.reader(f)
        for row in reader:
            data.append(row)

    return data


def statistics(list):
    '''
    功能:
        统计列表中字符出现的次数
    输入:
        list : 要统计的列表
    输出:
        frequency : 字典格式
    '''
    frequency = {}

    for word in list:
        if word not in frequency:
            frequency[word] = 1
        else:
            frequency[word] += 1

    return frequency


def path_split(
    path='/media/lcq/样本库/铁路标注数据/保定/白天/＜30/平交道口/人/JPEGImages/001903.jpg',
    # path='/media/lcq/样本库/铁路标注数据/客技站/白天/50/轨面/Annotations'
    ):

    '''
    功能
        根据图片的文件路径提取关键词
    输入
        path ：图片路径
    输出
        关键词列表
    '''

    path_split = path.split('/')
    img_name = path_split[-1]
    location = path_split[-7]
    sunshine = path_split[-6]
    distance = path_split[-5]
    scene    = path_split[-4]
    target   = path_split[-3]

    keys = [
        # path,
        img_name,
        location,
        sunshine,
        distance,
        scene,
        target]

    return keys


def test_get():
    
    # 测试路径
    # dir_name = 'dataset/'
    
    # 样本库测试路径
    # dir_name = '/media/lcq/样本库/铁路标注数据/保定'
    # dir_name = '/media/lcq/样本库/铁路标注数据/东郊'
    # dir_name = '/media/lcq/样本库/铁路标注数据/客技站'
    # dir_name = '/media/lcq/样本库/铁路标注数据/马鞍山'
    dir_name = '/media/lcq/样本库/铁路标注数据/亦庄'

    images_path = get_dir_file(dir_name)
    images_num = len(images_path)

    # ===================info ===================
    print('dir path  : {}'.format(dir_name))
    print('file num  : {}'.format(images_num))

    all_keys = []

    for i in range(images_num):

        keys = path_split(images_path[i])
        all_keys.append(keys)
        
        print('--{}/{}:{}'.format(i,images_num,keys))

    writer_csv('railSample_yz.csv', all_keys)


def test_read():

    csv_file = '/media/lcq/Data/modle_and_code/DataSet/RailSample/railSample.csv'

    headers = [
        'img_name',  # 文件名
        'location',  # 采集地点
        'sunshine',  # 采集时间
        'camera',    # 摄像机类型
        'distance',  # 距离
        'scene',     # 场景
        'target']    # 目标

    print('================== Start ==================')

    all_keys = read_csv(csv_file)
    all_keys = np.array(all_keys)

    # img_names = all_keys[:,0]
    locations = all_keys[:,1]
    sunshines = all_keys[:,2]
    cameras   = all_keys[:,3]
    distances = all_keys[:,4]
    scenes    = all_keys[:,5]
    targets   = all_keys[:,6]

    print('总图片数量  :{}'.format(len(all_keys)))
    print('采集地点   : {}'.format(statistics(locations)))
    print('采集时间   : {}'.format(statistics(sunshines)))
    print('摄像机类型 : {}'.format(statistics(cameras)))
    print('目标距离   : {}'.format(statistics(distances)))
    print('图像场景   : {}'.format(statistics(scenes)))
    print('目标类型   : {}'.format(statistics(targets)))

    print('=================== End ===================')


if __name__ == '__main__':
    test_read()