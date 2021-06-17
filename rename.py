#===================================================================
# 功能：重命名labels的名称，去掉名称里的_P，保证labels和images的名称一致
# LICHUAN
# lc@dlc618.com
# 参考：https://www.freesion.com/article/4723305868/
#===================================================================


import os,sys
 
cur_path = 'D:/camvid/camvid/labels' # 你的数据集路径
 
labels = os.listdir(cur_path)
 
for label in labels:
    old_label = str(label)
    new_label = label.replace('_P.png','.png')
    print(old_label, new_label)
    os.rename(os.path.join(cur_path,old_label),os.path.join(cur_path,new_label))