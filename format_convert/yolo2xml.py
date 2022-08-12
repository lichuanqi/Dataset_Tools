#  将yolo格式txt标注文件转换为voc格式xml标注文件

from xml.dom.minidom import Document
import os,glob,shutil
import cv2

from dataset_names import get_FSOD_dic


def makexml(picPath, 
            picPath_new, 
            dic,
            txtPath, 
            xmlPath):  # txt所在文件夹路径，xml文件保存路径，图片所在文件夹路径

    if not os.path.exists(xmlPath):
        os.mkdir(xmlPath)

    files = glob.glob(txtPath + '*.txt')
    num = len(files)

    print('共 {} 张图片'.format(num))

    for i, file in enumerate(files):

        name = file.split('\\')[-1].split('.')[0]       # 获取图片名字
        jpg_old = picPath + name + '.jpg'               # 图片旧路径
        xml = xmlPath + name + '.xml'
        
        if picPath_new:
            jpg_new = picPath_new + name + '.png'       # 图片新路径       
            shutil.copy(jpg_old, jpg_new)

        print('{}/{}:{} ...'.format(i+1, num, name))
        
        xmlBuilder = Document()
        annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
        xmlBuilder.appendChild(annotation)
        txtFile = open(file)
        txtList = txtFile.readlines()
        
        img = cv2.imread(jpg_old)
        Pheight, Pwidth, Pdepth = img.shape

        folder = xmlBuilder.createElement("folder")  # folder标签
        foldercontent = xmlBuilder.createTextNode("FSOD")
        folder.appendChild(foldercontent)
        annotation.appendChild(folder)  # folder标签结束

        filename = xmlBuilder.createElement("filename")  # filename标签
        filenamecontent = xmlBuilder.createTextNode(name + ".jpg")
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

        for j in txtList:
            oneline = j.strip().split(' ')
            print('--', oneline)
            object = xmlBuilder.createElement("object")              # object 标签
            picname = xmlBuilder.createElement("name")                    # name标签
            # namecontent = xmlBuilder.createTextNode(dic.get(oneline[0]))      # name标签内容
            namecontent = xmlBuilder.createTextNode(oneline[1])      # name标签内容
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

            # x_ = float(oneline[1])
            # y_ = float(oneline[2])
            # w_ = float(oneline[3])
            # h_ = float(oneline[4])

            # x1 = int(Pwidth * x_ - 0.5 * Pwidth * w_)
            # x2 = int(Pwidth * x_ + 0.5 * Pwidth * w_)
            # y1 = int(Pheight * y_ - 0.5 * Pheight * h_)
            # y2 = int(Pheight * y_ + 0.5 * Pheight * h_)

            x1 = int(oneline[2])
            y1 = int(oneline[3])
            x2 = int(oneline[4])
            y2 = int(oneline[5])

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

        f = open(xml, 'w')
        xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
        f.close()


if __name__ == "__main__":

    # 图片所在文件夹路径
    picPath = 'D:/CodePost/Xray_FSOD/X-ray FSOD/test/images/'
    # yolo txt所在文件夹路径
    txtPath = 'D:/CodePost/Xray_FSOD/X-ray FSOD/test/annotations/'
    
    # 标签和id对应关系
    dic = get_FSOD_dic()

    # 原始图片文件名修改然后复制一份到指定路径
    picPath_new = ''
    # xml文件保存路径
    xmlPath = 'D:/CodePost/Xray_FSOD/X-ray FSOD/test/xmls/'
    
    makexml(picPath, picPath_new, dic, txtPath, xmlPath)
