import os
import sys

from flask import Flask, flash, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import yolodetect as yolo
from quickdraw import QuickDrawData


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
# 사용자 입력 이미지 저장 디렉터리
UPLOAD_DIR = os.path.join(CURR_DIR, 'upload')
# 낙서 이미지 보낼 때 임시 저장 디렉터리
TEMP_DIR = os.path.join(CURR_DIR, 'temp')
# 연구실 com path: open("C:\\Users\\MR Lab\\Documents\\drawing-doodle-bot\\output.txt",'w')
OUTPUT_FILE = "/Users/superyodi/Documents/develop/doodle-bot/doodle-drawing-bot/pyflask/dobot_coord.txt"

if not os.path.exists(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR


# 확장자 check
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return 'Hello Flask'


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

            # 이미지로 욜로를 돌림
            label = yolo.extract_label(img_path)
            if len(label) > 0:
                return jsonify({'success': True, 'label': label})
            return jsonify({'success': False})


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


# doodleApp에서 낙서선택 버튼을 누르면 label, index return
# label, index -> dataset[label, indx]의 좌표값을 txt에 저장
@app.route('/draw/', methods=['GET'])
def draw_doodle():
    label = request.args.get('label')
    index = request.args.get('index')

    try:
        doodle = QuickDrawData().get_drawing(label, int(index))
    except:
        return jsonify({'success': False})

    make_coord(doodle)
    return jsonify({'success': True})


def make_coord(doodle):
    # 파일을 열고 write
    with open(OUTPUT_FILE, 'w') as f:
        for stroke in doodle.strokes:
            for x, y in stroke:
                d_x = int(x / 2 + 180)
                d_y = int(y / 2 - 80)
                f.write('%d %d\n' % (d_x, d_y,))
            f.write('\n')
