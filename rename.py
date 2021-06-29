#===================================================================
# 功能：重命名labels的名称，去掉名称里的_P，保证labels和images的名称一致
# LICHUAN
# lc@dlc618.com
# 参考：https://www.freesion.com/article/4723305868/
#===================================================================


import os,sys

def rename_label():
    # 你的数据集路径
    cur_path = '/media/lcq/Data/modle_and_code/DataSet/RailSample/JPEGImages'

    labels = os.listdir(cur_path)
    
    for label in labels:
        old_label = str(label)
        new_label = label.replace('_P.png','.png')
        print(old_label, new_label)
        os.rename(os.path.join(cur_path,old_label),os.path.join(cur_path,new_label))

    return 'Finished'


def rename_file():
    # 你的数据集路径
    path = '/media/lcq/Data/modle_and_code/DataSet/RailSample/JPEGImages'
    files = os.listdir(path)
    
    print('============= Start =============')
    print('File Numners: %s'%(len(files)))

    for file in files:
        old_label = str(file)
        new_label = file.split('；')[0] + '.' + file.split('.')[1]
        print(old_label + ' > ' + new_label)
        os.rename(os.path.join(path,old_label),os.path.join(path,new_label))

    print('============== End ==============')

    return 'Finshed'


if __name__=='__main__':
    rename_file()