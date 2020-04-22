from quickdraw import QuickDrawData
import sys


qd = QuickDrawData()

ant = qd.get_drawing("ant")


ant.image.show("ant.png")

sys.stdout = open("C:\\Users\\MR Lab\\Documents\\drawing-doodle-bot\\output.txt",'w')
for stroke in ant.strokes:
    for x, y in stroke:
        d_x = int(x/2 + 180)
        d_y = int(y/2 - 80)
        print(d_x,d_y)
        # print("x={} y={}".format(x, y))
    print("")

# def map_cordinate(x, y)