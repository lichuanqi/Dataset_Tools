# 统计COCO数据集各个类别的图片数和标注框数
# 未测试


from pycocotools.coco import COCO


dataDir='./COCO'
dataType='val2017'
#dataType='train2017'
annFile='{}/annotations/instances_{}.json'.format(dataDir, dataType)
 
# initialize COCO api for instance annotations
coco=COCO(annFile)
 
# display COCO categories and supercategories
cats = coco.loadCats(coco.getCatIds())
cat_nms=[cat['name'] for cat in cats]
print('number of categories: ', len(cat_nms))
print('COCO categories: \n', cat_nms)
 
# 统计各类的图片数量和标注框数量
for cat_name in cat_nms:
    catId = coco.getCatIds(catNms=cat_name)     # 1~90
    imgId = coco.getImgIds(catIds=catId)        # 图片的id  
    annId = coco.getAnnIds(catIds=catId)        # 标注框的id
 
    print("{:<15} {:<6d}     {:<10d}".format(cat_name, len(imgId), len(annId)))