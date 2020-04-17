from quickdraw import QuickDrawData

qd = QuickDrawData()

ant = qd.get_drawing("ant")
print(ant)

ant.image.show("ant.png")
print(type(ant.strokes))


for stroke in ant.strokes:
    for x, y in stroke:
        d_x = int(x/2 + 180)
        d_y = int(y/2 - 80)
        print(d_x, d_y)
        # print("x={} y={}".format(x, y))
    print("\n")

# def map_cordinate(x, y)