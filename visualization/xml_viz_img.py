# xml标注数据可视化

import xml.etree.ElementTree as ET
import os, cv2

imgfile  = 'D:/CodePost/Xray_all/jpgs/PIXray_143345099.jpg'
xml_file = 'D:/CodePost/Xray_all/xmls/PIXray_143345099.xml'

is_save = False 
save_path = 'C:/Users/00/Desktop/VMRD V2 fixed/visualization/'

im = cv2.imread(imgfile)
tree = ET.parse(xml_file)
root = tree.getroot()

for object in root.findall('object'):
    object_name = object.find('name').text
    Xmin = int(object.find('bndbox').find('xmin').text)
    Ymin = int(object.find('bndbox').find('ymin').text)
    Xmax = int(object.find('bndbox').find('xmax').text)
    Ymax = int(object.find('bndbox').find('ymax').text)
    print(object)
    color = (0, 0, 255)
    cv2.rectangle(im, (Xmin, Ymin), (Xmax, Ymax), color, 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(im, object_name, (Xmin, Ymin - 7), font, 0.5, (6, 230, 230), 2)

if is_save:
    cv2.imwrite('C:/Users/00/Desktop/VMRD V2 fixed/guyue/00077-ob.jpg', im)

cv2.imshow('img', im)
cv2.waitKey(0)