import glob
import os
import yaml


def box_data_prepare():
    """
    垃圾分类数据集GarbageClassify挑选指定类别的图片
    """

    anno_path = 'D:/Data/GarbageClassify/train_data/'
    annos = glob.glob(anno_path + '*.txt')
    savepath = 'D:/Data/GarbageClassify/box.yaml'

    # 遍历所有文件名报名所有标签名
    labels = {}
    imgs = {'20':[], '30':[]}

    for anno in annos:
        print(anno)

        with open(anno, 'r') as f:
            lines = f.readlines()
            for line in lines:
                label = line.split(' ')[1]

                # 统计每个类别的数量
                if label in labels.keys():
                    labels[label] += 1
                else:
                    labels[label] = 0

                # 保存包含指定标签的文件名
                # TODO: 去除重复
                if label in imgs.keys():
                    imgs[label].append(anno)

    print('信息统计算完毕：')
    for key,value in labels.items():
        print('--{: <15}: {}'.format(key, value))

    with open(savepath, 'w') as f:
        yaml.dump(imgs, f)
    print(f'结果保存至：{savepath}')


def FSOD_data_prepare():
    """
    统计X-ray FSOD数据集各类别的数量
    """

    txt_path = 'D:/CodePost/Xray_FSOD/X-ray FSOD/train/annotations/'
    txts = os.listdir(txt_path)

    # 遍历所有文件名报名所有标签名
    labels = [] 
    for txt in txts:

        with open(txt_path + txt, 'r') as f:
            lines = f.readlines()
            for line in lines:
                label = line.split(' ')[1]
                labels.append(label)

    labels_num = {} 

    for name in labels:

        if name not in labels_num.keys():
            labels_num[name] = 1
        else:
            labels_num[name] += 1

    print('信息统计算完毕：')
    for key,value in labels_num.items():
        print('--{: <15}: {}'.format(key, value))


if __name__ == '__main__':
    box_data_prepare()
