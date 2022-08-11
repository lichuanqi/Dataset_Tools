# 真主要针对X-ray FSOD的特殊标注文件格式，统计各类别情况

from cProfile import label
import os

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
