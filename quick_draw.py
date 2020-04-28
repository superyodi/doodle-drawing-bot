
from quickdraw import QuickDrawData
import sys
import yolodetect as yolo

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


try:
    label = yolo.label
    dataset = qd.get_drawing(label)
    dataset.image.show("dataset.png")
    dataset.image.save("dataset.png")
except:
    print("객체를 찾을 수 없습니다.")

mapCoord(dataset)

# with open("coco.names", "r") as f:
#     labels = [line.strip() for line in f.readlines()]
#
#     sys.stdout = open("labels.txt", 'w')
#     for label in labels:
#         if label in qd.drawing_names:
#             print(label)


# def map_cordinate(x, y)