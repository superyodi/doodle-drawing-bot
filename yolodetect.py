
# -*- coding: utf-8 -*-≤

import cv2
import numpy as np

#Load Yolo
net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
classes = []

with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Load img
img = cv2.imread("sample_images/sheep.jpg")

img = cv2.resize(img, None, fx = 0.4, fy = 0.4)
height, width, channels = img.shape

# Detect objects
blob = cv2.dnn.blobFromImage(img, 0.004, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layers)

#Show information on the screen
class_ids = []
confidences = []
boxes = []
tmp_confidence = 0

for out in outs:
    for detection in out:
        # detect the confidence, How correct the algorithm
        scores = detection[5:]
        class_id = np.argmax(scores)
        #scores를 최댓값으로 만들기 위한
        confidence = scores[class_id]
        if confidence > 0.5:
            # 객체 인식
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # Rectangle coordinate, 사각형 좌표
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# confidence가 더 높은 boxes
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.6, 0.4)

font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = classes[class_ids[i]]
        print(label)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, label, (x, y + 30), font, 1, (255, 255, 255), 1)

cv2.imshow("Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()






