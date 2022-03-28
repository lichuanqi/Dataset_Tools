# -*- coding: utf-8 -*-
# 根据 xml 标签文件求先验框
# 参考：

from contextlib import redirect_stderr
import os
import re
from tkinter import W
import xml.etree.cElementTree as et

from cv2 import ROTATE_90_COUNTERCLOCKWISE
import numpy as np
from matplotlib import pyplot as plt 


def iou(box, clusters):
    """
    Calculates the Intersection over Union (IoU) between a box and k clusters.
    :param box: tuple or array, shifted to the origin (i. e. width and height)
    :param clusters: numpy array of shape (k, 2) where k is the number of clusters
    :return: numpy array of shape (k, 0) where k is the number of clusters
    """
    x = np.minimum(clusters[:, 0], box[0])
    y = np.minimum(clusters[:, 1], box[1])
    if np.count_nonzero(x == 0) > 0 or np.count_nonzero(y == 0) > 0:
        raise ValueError("Box has no area")                 # 如果报这个错，可以把这行改成pass即可
    intersection = x * y
    box_area = box[0] * box[1]
    cluster_area = clusters[:, 0] * clusters[:, 1]
    iou_ = intersection / (box_area + cluster_area - intersection)
    return iou_
def avg_iou(boxes, clusters):
    """
    Calculates the average Intersection over Union (IoU) between a numpy array of boxes and k clusters.
    :param boxes: numpy array of shape (r, 2), where r is the number of rows
    :param clusters: numpy array of shape (k, 2) where k is the number of clusters
    :return: average IoU as a single float
    """
    return np.mean([np.max(iou(boxes[i], clusters)) for i in range(boxes.shape[0])])
def translate_boxes(boxes):
    """
    Translates all the boxes to the origin.
    :param boxes: numpy array of shape (r, 4)
    :return: numpy array of shape (r, 2)
    """
    new_boxes = boxes.copy()
    for row in range(new_boxes.shape[0]):
        new_boxes[row][2] = np.abs(new_boxes[row][2] - new_boxes[row][0])
        new_boxes[row][3] = np.abs(new_boxes[row][3] - new_boxes[row][1])
    return np.delete(new_boxes, [0, 1], axis=1)
def kmeans(boxes, k, dist=np.median):
    """
    Calculates k-means clustering with the Intersection over Union (IoU) metric.
    :param boxes: numpy array of shape (r, 2), where r is the number of rows
    :param k: number of clusters
    :param dist: distance function
    :return: numpy array of shape (k, 2)
    """
    rows = boxes.shape[0]
    distances = np.empty((rows, k))
    last_clusters = np.zeros((rows,))
    np.random.seed()
    # the Forgy method will fail if the whole array contains the same rows
    clusters = boxes[np.random.choice(rows, k, replace=False)]
    while True:
        for row in range(rows):
            distances[row] = 1 - iou(boxes[row], clusters)
        nearest_clusters = np.argmin(distances, axis=1)
        if (last_clusters == nearest_clusters).all():
            break
        for cluster in range(k):
            clusters[cluster] = dist(boxes[nearest_clusters == cluster], axis=0)
        last_clusters = nearest_clusters
    return clusters


def load_data_from_xml(anno_dir, class_names):

    xml_names = os.listdir(anno_dir)
    boxes = []

    for xml_name in xml_names:

        xml_pth = os.path.join(anno_dir, xml_name)
        tree = et.parse(xml_pth)

        width = float(tree.findtext("./size/width"))
        height = float(tree.findtext("./size/height"))
        
        for obj in tree.findall("./object"):
            cls_name = obj.findtext("name")
            if cls_name in class_names:
                xmin = float(obj.findtext("bndbox/xmin")) / width
                ymin = float(obj.findtext("bndbox/ymin")) / height
                xmax = float(obj.findtext("bndbox/xmax")) / width
                ymax = float(obj.findtext("bndbox/ymax")) / height
                box = [xmax - xmin, ymax - ymin]
                boxes.append(box)
            else:
                continue

    return np.array(boxes)


def load_wh_from_xml(anno_dir, class_names):
    """
    从 xml 文件中读取目标框的 宽度w 和 高度h
    """

    xml_names = os.listdir(anno_dir)
    boxes = []

    for xml_name in xml_names:

        xml_pth = os.path.join(anno_dir, xml_name)
        tree = et.parse(xml_pth)

        width = float(tree.findtext("./size/width"))
        height = float(tree.findtext("./size/height"))
        
        for obj in tree.findall("./object"):
            cls_name = obj.findtext("name")
            if cls_name in class_names:
                xmin = int(obj.findtext("bndbox/xmin"))
                ymin = int(obj.findtext("bndbox/ymin"))
                xmax = int(obj.findtext("bndbox/xmax")) 
                ymax = int(obj.findtext("bndbox/ymax"))
                box = [xmax - xmin, ymax - ymin]
                boxes.append(box)
            else:
                continue

    return np.array(boxes)


def scatter_by_wh(ANNOTATION_PATH,                        # 数据集xml标签文件夹路径
                  IS_SAVE=False,
                  CLASS_NAMES=['person','train'] ):
    """
    根据目标框的宽度和高度绘制散点图
    """

    ancnhors_x = [3, 4, 6, 9, 13, 18, 32, 57, 98]
    ancnhors_y = [13, 21, 30, 37, 56, 85, 143, 57, 292]

    train_boxes = load_wh_from_xml(ANNOTATION_PATH, CLASS_NAMES)
    
    w = []
    h = []

    for i in train_boxes:
        w.append(i[0])
        h.append(i[1])

    plt.figure()
    # 矩形框
    plt.scatter(w,h,alpha=0.6)
    # anchors
    plt.scatter(ancnhors_x,ancnhors_y,c='r',marker='s')
    plt.xlabel('Width')
    plt.xlabel('Height')
    plt.xlim(-10,1920)
    plt.ylim(-10,1080)
    plt.minorticks_on()
    # plt.savefig('D:/论文/论文3-毕业论文/图片/图 37-目标框散点图.jpg',dpi=300, bbox_inches='tight')
    plt.show()

    return True


def get_anchors_by_kmeans(ANNOTATION_PATH,                        # 数据集xml标签文件夹路径
                          ANCHORS_TXT_PATH,                       # anchors.txt 文件保存位置
                          CLUSTERS = 9,                           # anchors数量
                          CLASS_NAMES = ['person','train'] ):     # 指定目标类别

    anchors_txt = open(ANCHORS_TXT_PATH, "w")
    train_boxes = load_data_from_xml(ANNOTATION_PATH, CLASS_NAMES)
    count = 1
    best_accuracy = 0
    best_anchors = []
    best_ratios = []

    # 可以修改，不要太大，否则时间很长
    for i in range(10):      
        anchors_tmp = []
        clusters = kmeans(train_boxes, k=CLUSTERS)
        idx = clusters[:, 0].argsort()
        clusters = clusters[idx]
        
        for j in range(CLUSTERS):
            anchor = [round(clusters[j][0] * 640, 2), round(clusters[j][1] * 640, 2)]
            anchors_tmp.append(anchor)
            print(f"Anchors:{anchor}")
        
        temp_accuracy = avg_iou(train_boxes, clusters) * 100
        print("Train_Accuracy:{:.2f}%".format(temp_accuracy))
        ratios = np.around(clusters[:, 0] / clusters[:, 1], decimals=2).tolist()
        ratios.sort()
        print("Ratios:{}".format(ratios))
        print(20 * "*" + " {} ".format(count) + 20 * "*")

        count += 1
        
        if temp_accuracy > best_accuracy:
            best_accuracy = temp_accuracy
            best_anchors = anchors_tmp
            best_ratios = ratios

    anchors_txt.write("Best Accuracy = " + str(round(best_accuracy, 2)) + '%' + "/n")
    anchors_txt.write("Best Anchors = " + str(best_anchors) + "/n")
    anchors_txt.write("Best Ratios = " + str(best_ratios))
    anchors_txt.close()


if __name__ == '__main__':

    # 设置参数
    ANNOTATION_PATH = 'D:/Code/DATASET/RailSample/xmls/'           # 数据集标签文件夹路径
    ANCHORS_TXT_PATH = "D:/Code/DATASET/RailSample/anchors.txt"   # anchors文件保存位置
    
    CLUSTERS = 9
    CLASS_NAMES = ['person','train']   #类别名称

    scatter_by_wh(ANNOTATION_PATH,
                  CLASS_NAMES)

    # 计算 anchors
    # get_anchors_by_kmeans(ANNOTATION_PATH,
    #                       ANCHORS_TXT_PATH,
    #                       CLUSTERS,
    #                       CLASS_NAMES)

   