# txt标注数据可视化

import os, cv2
import numpy as np


imgfile  = "D:/CodePost/Xray_FSOD/X-ray FSOD/test/images/00787.jpg"
txt_file = 'D:/CodePost/Xray_FSOD/X-ray FSOD/test/annotations/00787.txt'
labels = [
    'laptop',
    'lighter',
    'portable_charger_2',
    'iron_shoe',
    'straight_knife',
    'folding_knife', 
    'scissor',
    'multi-tool_knife',
    'umbrella',
    'glass_bottle',
    'battery',
    'metal_cup',
    'nail_clippers',
    'pressure_tank',
    'spray_alcohol',
    'portable_charger_1',
    'utility_knife', 
    'mobile_phone',
    'metal_can',
    'drink_bottle']


font = cv2.FONT_HERSHEY_SIMPLEX
is_save = False 
save_path = ''

im = cv2.imread(imgfile)
h, w, n = im.shape


with open(txt_file, 'r') as f:
    # 将txt中的数据逐行存到列表lines里 lines的每一个元素对应于txt中的一行。
    # 然后将每个元素中的不同信息提取出来
    lines = f.readlines()
    for line in lines:


        label_name = line.split(' ')[1]
        x1 = int(line.split(' ')[2])
        y1 = int(line.split(' ')[3])
        x2 = int(line.split(' ')[4])
        y2 = int(line.split(' ')[5])
        
        # label_id = int(line.split(' ')[0])
        # x_ = float(line.split(' ')[1])
        # y_ = float(line.split(' ')[2])
        # w_ = float(line.split(' ')[3])
        # h_ = float(line.split(' ')[4])
        
        # label_name = labels[label_id]

        # x1 = int(w * x_ - 0.5 * w * w_)
        # x2 = int(w * x_ + 0.5 * w * w_)
        # y1 = int(h * y_ - 0.5 * h * h_)
        # y2 = int(h * y_ + 0.5 * h * h_)
        
        color = (4, 250, 7)
        draw = cv2.rectangle(im,(x1,y1),(x2,y2),color,2)
        cv2.putText(im, label_name, (x1, y1 - 7), font, 0.5, color, 2)

if is_save:
    
    cv2.imwrite(save_path, im)

cv2.imshow('img', im)
cv2.waitKey(0)