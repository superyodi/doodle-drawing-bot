from quickdraw import QuickDrawData
qd = QuickDrawData()
car = qd.get_drawing("car")
face = qd.get_drawing("face")
# car.image.save("car.jpg")
car.image.show()
face.image.show()

print(qd.drawing_names)