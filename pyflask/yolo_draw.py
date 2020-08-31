import time
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
from quickdraw import QuickDrawData


class DrawDoodle:
    def __init__(self):

        self.img_path = None
        self.img = None
        self.height = None
        self.width = None
        self.channels = None
        self.d_strokes = None

    def setImgPath(self, img_path):
        img = cv2.imread(img_path)

        self.img_path = img_path
        self.img = img
        height, width, channels = img.shape
        self.height = height
        self.width = width
        self.channels = channels



    def make_dobotCoord(self, output_file):

        with open(output_file, 'w') as f:
            for stroke in self.d_strokes:
                for x, y in stroke:
                    f.write('%d %d\n' % (x, y))
                f.write('\n')

    def draw_chart(self):
        img2 = self.make_doodleImg()
        img1 = self.make_detectedImg()

        fig = plt.figure()
        rows = 1
        cols = 2

        ax1 = fig.add_subplot(rows, cols, 1)
        ax1.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
        ax1.set_title('YOLO detected Image')
        ax1.axis("off")

        ax2 = fig.add_subplot(rows, cols, 2)
        ax2.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
        ax2.set_title('created by doodle Image')
        ax2.axis("off")

        plt.show()

    def make_doodleImg(self):
        img_doodle = np.full((self.height, self.width, 3), 255, dtype=np.uint8)

        self.detect_obect(img_doodle, 1)

        # '{}/{}'.format(read_dir, file)
        cv2.imwrite('{}_{}.png'.format("doodle", "00"), img_doodle)
        return img_doodle

    def make_detectedImg(self):
        self.detect_obect(self.img, 0)
        cv2.imwrite('{}_{}.png'.format("detected", "00"), self.img)

        return self.img

    def draw_person(self, img, d_w0, d_h0, d_w, d_h):
        self.draw_doodle(img, "face", d_w0, d_h0, d_w, d_h // 3)
        # 상의
        self.draw_doodle(img, "t-shirt", d_w0, d_h0+d_h//3, d_w, d_h//3)
        # 하의
        self.draw_doodle(img, "pants", d_w0, d_h0 + 2* d_h//3, d_w, d_h//3)

    # 낙서 그림 그리기
    def draw_doodle(self, img, label, d_w0, d_h0, d_w, d_h):

        idx = random.randrange(0, 999)
        doodle = QuickDrawData().get_drawing(label, idx)

        # 낙서 그릴때 dobot_coord.txt도 동시에 만든다.
        if self.d_strokes is None:
            self.d_strokes = []

        # with open(self.OUTPUT_FILE, 'w') as f:
        for stroke in doodle.strokes:
            d_points = []
            for i in range(0, len(stroke)-1):
                x = int(d_w * stroke[i][0] / 255) + d_w0
                y = int(d_h * stroke[i][1] / 255) + d_h0

                pre_x = int(d_w * stroke[i+1][0]/ 255) + d_w0
                pre_y = int(d_h * stroke[i+1][1] / 255) + d_h0

                cv2.line(img, (pre_x, pre_y), (x, y), (255, 0, 0), 2)

                d_x = int((x / self.width * 255) / 2 + 180)
                d_y = int((y / self.height * 255) / 2 - 80)
                d_points.append((d_x, d_y))
                # f.write('%d %d\n' % (d_x, d_y,))

                if i == len(stroke)-2:
                    x = int(d_w * stroke[i+1][0] / 255) + d_w0
                    y = int(d_h * stroke[i+1][1] / 255) + d_h0
                    d_x = int((x / self.width * 255) / 2 + 180)
                    d_y = int((y / self.height * 255) / 2 - 80)
                    d_points.append((d_x, d_y))
                    # f.write('%d %d\n' % (d_x, d_y,))

            # f.write('\n')
            self.d_strokes.append(d_points)

    # flag: 0 -> make detected img, flag: 1 -> make doodle img
    def detect_obect(self, out_img, flag):

        # Load Yolo
        net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
        classes = []

        with open("coco.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]

        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        height, width, channels = self.height, self.width, self.channels
        img = self.img


        # Detect objects
        blob = cv2.dnn.blobFromImage(img, 0.004, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Show information on the screen
        class_ids = []
        confidences = []
        boxes = []
        tmp_confidence = 0

        for out in outs:
            for detection in out:
                # detect the confidence, How correct the algorithm
                scores = detection[5:]
                class_id = np.argmax(scores)
                # scores를 최댓값으로 만들기 위한
                confidence = scores[class_id]
                if confidence > 0.3:
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
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.6)

        # show detected iamge
        # with open(self.OUTPUT_FILE, 'w') as f:
        for i in range(len(boxes)):
            # print("good?")
            if i in indexes:
                x, y, w, h = boxes[i]
                label = classes[class_ids[i]]
                print(label)
                if flag == 1:
                    try:
                        self.draw_doodle(out_img, label, x, y, w, h)
                    except:
                        if label == "person":
                            self.draw_person(out_img, x, y, w, h)
                        else:
                            print("해당하는 낙서가 없습니다.")
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    font = cv2.FONT_HERSHEY_PLAIN
                    cv2.putText(img, label, (x, y + 30), font, 1, (255, 255, 255), 1)



# confidence 값에 대한 bounding box 결과 확인하기
# def trackbar2(x):
#     confidence = x/100
#     r = r0.copy()
#     for output in np.vstack(outs):
#         if output[4] > confidence:
#             x, y, w, h = output[:4]
#             print(x, y, w, h)
#             p0 = int((x-w/2)*416), int((y-h/2)*416)
#             p1 = int((x+w/2)*416), int((y+h/2)*416)
#             cv2.rectangle(r, p0, p1, 1, 1)
#     cv2.imshow('blob', r)
#     text = f'Bbox confidence={confidence}'
#     cv2.displayOverlay('blob', text)
#
# r0 = blob[0, 0, :, :]
# r = r0.copy()
# cv2.imshow('blob', r)
# cv2.createTrackbar('confidence', 'blob', 50, 101, trackbar2)
# trackbar2(50)
# cv2.waitKey(0)