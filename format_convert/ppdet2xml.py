"""
PaddleDetection动态图预测结果转换为labelImg的xml格式
lichuanqi
lc@dlc618.com
2022.11.13 15:35
"""

import os
import json
from xml.dom.minidom import Document

import cv2


def generate_xml_by(img_name,
                    xml_name,
                    Pheight,
                    Pwidth,
                    Pdepth,
                    boxes) -> None:
    """生成labelImg的标注文件

    Params
        img_name                : 图片文件名
        xml_name                : 标签名
        Pheight, Pwidth, Pdepth : 图片的高度、宽度、通道数
        boxes                   : [[label_name x1 y1 x2 y2]]
    Output
        xml_name.xml
    """

    # 测试数据
    # xml_name = 'D:/Data/Expressbox/images_test/1.xml'
    # img_name = 'D:/Data/Expressbox/images_test/1.jpg'
    # Pheight, Pwidth, Pdepth = 1080, 1920, 3
    # boxes = [['', 'box', 1960.350341796875, 1210.6590576171875, 2880.8642578125,2070.91796875]]

    xmlBuilder = Document()
    annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
    xmlBuilder.appendChild(annotation)

    folder = xmlBuilder.createElement("folder")  # folder标签
    foldercontent = xmlBuilder.createTextNode("FSOD")
    folder.appendChild(foldercontent)
    annotation.appendChild(folder)  # folder标签结束

    filename = xmlBuilder.createElement("filename")  # filename标签
    filenamecontent = xmlBuilder.createTextNode(img_name)
    filename.appendChild(filenamecontent)
    annotation.appendChild(filename)  # filename标签结束

    size = xmlBuilder.createElement("size")  # size标签
    width = xmlBuilder.createElement("width")  # size子标签width
    widthcontent = xmlBuilder.createTextNode(str(Pwidth))
    width.appendChild(widthcontent)
    size.appendChild(width)  # size子标签width结束

    height = xmlBuilder.createElement("height")  # size子标签height
    heightcontent = xmlBuilder.createTextNode(str(Pheight))
    height.appendChild(heightcontent)
    size.appendChild(height)  # size子标签height结束

    depth = xmlBuilder.createElement("depth")  # size子标签depth
    depthcontent = xmlBuilder.createTextNode(str(Pdepth))
    depth.appendChild(depthcontent)
    size.appendChild(depth)  # size子标签depth结束

    annotation.appendChild(size)  # size标签结束

    for oneline in boxes:
        object = xmlBuilder.createElement("object")              # object 标签
        picname = xmlBuilder.createElement("name")                    # name标签
        # namecontent = xmlBuilder.createTextNode(dic.get(oneline[0]))      # name标签内容
        namecontent = xmlBuilder.createTextNode(oneline[0])      # name标签内容
        picname.appendChild(namecontent)
        object.appendChild(picname)                                   # name标签结束

        pose = xmlBuilder.createElement("pose")  # pose标签
        posecontent = xmlBuilder.createTextNode("Unspecified")
        pose.appendChild(posecontent)
        object.appendChild(pose)  # pose标签结束

        truncated = xmlBuilder.createElement("truncated")  # truncated标签
        truncatedContent = xmlBuilder.createTextNode("0")
        truncated.appendChild(truncatedContent)
        object.appendChild(truncated)  # truncated标签结束

        difficult = xmlBuilder.createElement("difficult")  # difficult标签
        difficultcontent = xmlBuilder.createTextNode("0")
        difficult.appendChild(difficultcontent)
        object.appendChild(difficult)  # difficult标签结束

        x1 = int(oneline[1])
        y1 = int(oneline[2])
        x2 = int(oneline[3])
        y2 = int(oneline[4])

        bndbox = xmlBuilder.createElement("bndbox")    # bndbox标签
        xmin = xmlBuilder.createElement("xmin")              # xmin标签

        # mathData = int(((float(oneline[1])) * Pwidth + 1) - (float(oneline[3])) * 0.5 * Pwidth)
        xminContent = xmlBuilder.createTextNode(str(x1))
        xmin.appendChild(xminContent)
        bndbox.appendChild(xmin)                             # xmin标签结束

        ymin = xmlBuilder.createElement("ymin")              # ymin标签
        # mathData = int(((float(oneline[2])) * Pheight + 1) - (float(oneline[4])) * 0.5 * Pheight)
        yminContent = xmlBuilder.createTextNode(str(y1))
        ymin.appendChild(yminContent)
        bndbox.appendChild(ymin)                             # ymin标签结束

        xmax = xmlBuilder.createElement("xmax")              # xmax标签
        # mathData = int(((float(oneline[1])) * Pwidth + 1) + (float(oneline[3])) * 0.5 * Pwidth)
        xmaxContent = xmlBuilder.createTextNode(str(x2))
        xmax.appendChild(xmaxContent)
        bndbox.appendChild(xmax)                             # xmax标签结束

        ymax = xmlBuilder.createElement("ymax")              # ymax标签
        # mathData = int(((float(oneline[2])) * Pheight + 1) + (float(oneline[4])) * 0.5 * Pheight)
        ymaxContent = xmlBuilder.createTextNode(str(y2))
        ymax.appendChild(ymaxContent)
        bndbox.appendChild(ymax)                             # ymax标签结束
        object.appendChild(bndbox)                     # bndbox标签结束
        annotation.appendChild(object)  # object标签结束

    with open(xml_name, 'w') as f:
        xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
    print(f'已保存 {xml_name}')


def dynamic2xml(image_dir, dynamic_json, id2name):
    """PaddleDetection动态图预测结果转换为labelImg的xml格式

    PaddleDetection动态图预测格式
    {
        "bbox": [
            [
                # x1 y1 x2 y2
                [1960.350341796875, 1210.6590576171875, 2880.8642578125, 2070.91796875]
            ],
            [
                [291.97430419921875, 273.5363464355469, 451.52490234375, 398.732666015625],
                [491.71234130859375, 150.89585876464844, 565.5228271484375, 220.06752014160156],
            ]
        ],
        "score": [
            [0.5832483172416687],
            [0.7591311931610107, 0.6562308669090271]
        ],
        "label": [
            [0.0],
            [0.0, 0.0]
        ]
    }

    Params
        image_dir (str)   : 预测的图片文件夹
        dynamic_json (str): PaddleDetection动态图预测结果路径
    """
    images = os.listdir(image_dir)
    print(f'共读取到 {len(images)} 个原始图片')

    with open(dynamic_json, 'r') as f:
        data = json.load(f)

    bbox = data['bbox']
    score = data['score']
    label = data['label']

    print(f'共读取到 {len(label)} 个图片的预测结果')

    # 确保预测的图片文件夹内图片的图像等于预测结果数量
    if len(images) != len(label):
        raise
    
    i = 0
    for _images, _bbox,_score,_label in zip(images, bbox, score, label):
        
        img_name = os.path.join(image_dir, _images)
        xml_name = img_name.replace('jpg', 'xml')
        Pheight, Pwidth, Pdepth = cv2.imread(img_name).shape
        boxes = []

        num = len(_label)
        print(f'{i}: {_images} 共 {num} 个预测框')

        for j in range(num):
            x1, y1, x2, y2 = _bbox[j][0], _bbox[j][1], _bbox[j][2], _bbox[j][3]
            conf = _score[j]
            la = int(_label[j])

            if conf >= 0.5:
                print(f'-- {la} {x1} {y1} {x2} {y2} {conf}')
                boxes.append([id2name[la], x1, y1, x2, y2])

        generate_xml_by(img_name,
                    xml_name,
                    Pheight,
                    Pwidth,
                    Pdepth,
                    boxes)

        i += 1


def static2xml():
    """PaddleDetection静态图预测结果转换为labelImg的xml格式

    感觉文件结构结构比较复杂比如用动态图的输出结果
    """
    pass


if __name__ == '__main__':
    image_dir = 'D:\Data\Expressbox\images_test'
    dynamic_json = "D:\Code\PADDLE\PaddleDetection\output\dynamic.json"
    id2name = {0: 'box'}
    dynamic2xml(image_dir, dynamic_json, id2name)