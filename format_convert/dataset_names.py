"""
常用数据集的 names.list
"""

import re


def get_coco_names():

    coco_names = [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
               'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
               'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
               'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
               'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
               'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
               'hair drier', 'toothbrush' ] 

    return coco_names


def get_coco_dict():

    coco_dict = {1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus', 7: 'train', 8: 'truck',
                9: 'boat', 10: 'traffic light', 11: 'fire hydrant', 13: 'stop sign', 14: 'parking meter', 15: 'bench',
                16: 'bird', 17: 'cat', 18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear', 24: 'zebra',
                25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag', 32: 'tie', 33: 'suitcase', 34: 'frisbee',
                35: 'skis', 36: 'snowboard', 37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
                41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle', 46: 'wine glass', 47: 'cup',
                48: 'fork', 49: 'knife', 50: 'spoon', 51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
                56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut', 61: 'cake', 62: 'chair', 63: 'couch',
                64: 'potted plant', 65: 'bed', 67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
                75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven', 80: 'toaster', 81: 'sink',
                82: 'refrigerator', 84: 'book', 85: 'clock', 86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier',
                90: 'toothbrush'}

    return coco_dict


def get_voc_names():

    voc_names  = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle',
                'bus', 'car', 'cat', 'chair', 'cow', 'diningtable',
                'dog', 'horse', 'motorbike', 'pottedplant',
                'sheep', 'sofa', 'train', 'tvmonitor', 'person']

    return voc_names


def get_rail14_names():

    railsample = ['person', 'bicycle', 'car', 'motorbike', 'tricycle', 'train', 'truck',
				  'forklift', 'bus', 'bag', 'dog', 'box', 'stone', 'light']

    return railsample


def get_rail2_names():

    railsample_2 = ['person', 'train']

    return railsample_2


def get_icig_names():

    labels_icig = [ 'pinA_normal', 'screw_normal', 'pinB_miss',
                'puller_normal', 'pinB_normal', 'pinD_latent',
                'pinD_normal', 'puller_miss', 'pinC_normal',
                'nut', 'screw_miss', 'pinA_miss',
                'pinD_miss', 'nut_normal', 'pinA_latent',
                'pinB_latent', 'pinC_miss', 'pinC_latent' ]

    return labels_icig


def get_FSOD_names():
    
    FSOD_names =  [
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

    return FSOD_names


def get_FSOD_dic():

    dic = {
    '0': 'laptop',
    '1': 'lighter',
    '2': 'portable_charger_2',
    '3': 'iron_shoe',
    '4': 'straight_knife',
    '5': 'folding_knife',
    '6': 'scissor',
    '7': 'multi-tool_knife',
    '8': 'umbrella',
    '9': 'glass_bottle',
    '10': 'battery',
    '11': 'metal_cup',
    '12': 'nail_clippers',
    '13': 'pressure_tank',
    '14': 'spray_alcohol',
    '15': 'portable_charger_1',
    '16': 'utility_knife',
    '17': 'mobile_phone',
    '18': 'metal_can',
    '19': 'drink_bottle'
    }  

    return dic


def get_xray13_names():

    xray13_names = ['laptop', 'portable_charger_2', 'mobile_phone', 'portable_charger_1',
     'battery', 'pressure_tank', 'lighter', 'straight_knife', 'folding_knife',
     'multi-tool_knife', 'utility_knife', 'Gun', 'Fireworks']

    return xray13_names
    

cityspace_names    = ["background","aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]



if __name__ == '__main__':

    FSOD_dic = get_FSOD_dic()

    print(FSOD_dic.get('0'))