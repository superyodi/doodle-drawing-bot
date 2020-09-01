import os
import sys

from flask import Flask, flash, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from yolo_draw import DrawDoodle
from quickdraw import QuickDrawData


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
# 사용자 입력 이미지 저장 디렉터리
UPLOAD_DIR = os.path.join(CURR_DIR, 'upload')
# 낙서 이미지 보낼 때 임시 저장 디렉터리
TEMP_DIR = os.path.join(CURR_DIR, 'temp')
# 객체 검출한 결과 이미지 저장 디렉터리
DETECTED_DIR = os.path.join(CURR_DIR, 'detected')
# 연구실 com path: open("C:\\Users\\MR Lab\\Documents\\drawing-doodle-bot\\output.txt",'w')
OUTPUT_FILE = "/Users/superyodi/Documents/develop/doodle-bot/doodle-drawing-bot/pyflask/dobot_coord.txt"

if not os.path.exists(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)

if not os.path.exists(DETECTED_DIR):
    os.mkdir(DETECTED_DIR)

app = Flask(__name__)
# run_with_ngrok(app)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

# Draw Doodle instance 선언
doodle = DrawDoodle()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)


# 확장자 check
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return 'Welcome to Doodle-Bot Server ;-)'


@app.route('/inspect/', methods=['GET', 'POST'])
def inspect():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'no file'})
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({'error': 'no file'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(img_path)

            doodle.setImgPath(img_path)

            filename = 'DETECTED_{}'.format(filename)
            new_img_path = os.path.join(DETECTED_DIR, filename)
            cv2.imwrite(new_img_path, doodle.make_detectedImg())

            return send_from_directory(DETECTED_DIR, filename)


# 낙서 찾기
@app.route('/doodle/', methods=['GET'])
def find_doodle():
    label = request.args.get('label')
    index = request.args.get('index')

    # label이 labels.txt에 존재하는지 확인
    # label에 맞는 낙서 img를 찾아서 key, img, status 보내기
    try:
        doodle = QuickDrawData().get_drawing(label, int(index))
    except:
        return jsonify({'success': False})

    print(TEMP_DIR)
    filename = '%s_%s.png' % (label, index,)
    doodle.image.save(os.path.join(TEMP_DIR, filename))

    return send_from_directory(TEMP_DIR, filename)

# 사진 받아서 낙서이미지 전송
@app.route('/doodles/', methods=['GET'])
def draw_doodles():
    imgPath = request.args.get('imgPath')
    print(imgPath)


    # image path에 해당하는 이미지를 찾는다.
    try:
        doodle.setImgPath('./upload/{}'.format(imgPath))
        doodle.d_strokes = None

    except:
        return jsonify({'error': 'Wrong file path'}), 400

    filename = 'DOODLED_{}'.format(imgPath)
    new_img_path = os.path.join(TEMP_DIR, filename)
    cv2.imwrite(new_img_path, doodle.make_doodleImg())

    return send_from_directory(TEMP_DIR, filename)


# doodleApp에서 낙서선택 버튼을 누르면 해당 낙서의 좌표값으 txt에 저장
@app.route('/draw/')
def draw_doodle():
    try:
        doodle.make_dobotCoord("./dobot_coord.txt")
        print("dobot_coord.txt 업로드 완료")
        return jsonify({'success': True})
    except:
        return jsonify({'sucess': False})







