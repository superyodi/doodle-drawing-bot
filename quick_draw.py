
from quickdraw import QuickDrawData
import sys
import yolodetect as yolo
import threading

count = 0

qd = QuickDrawData()

def mapCoord(ds):
    sys.stdout = open("C:\\Users\\MR Lab\\Documents\\drawing-doodle-bot\\output.txt",'w')
    for stroke in ds.strokes:
        for x, y in stroke:
            d_x = int(x/2 + 180)
            d_y = int(y/2 - 80)
            print(d_x,d_y)
            # print("x={} y={}".format(x, y))
        print("")

def choiceDraw(l):
    data_set = qd.get_drawing(l)
    data_set.image.show("dataset.png")
    check = input("a를 눌러 낙서를 선택하세요 ")
    print(check)


    while check != 'a':
        data_set = qd.get_drawing(l)
        data_set.image.show("dataset.png")
        check = input("a를 눌러 낙서를 선택하세요 ")

    return data_set

try:
    label = yolo.label
except:
    print("객체를 찾을 수 없습니다.")

dataset = choiceDraw(label)
    # dataset = qd.get_drawing(label)
    # dataset.image.show("dataset.png")
dataset.image.save("dataset.png")
mapCoord(dataset)



# with open("coco.names", "r") as f:
#     labels = [line.strip() for line in f.readlines()]
#
#     sys.stdout = open("labels.txt", 'w')
#     for label in labels:
#         if label in qd.drawing_names:
#             print(label)


# def map_cordinate(x, y)