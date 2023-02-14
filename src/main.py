from flask import Flask, render_template, request, redirect, Markup
from flask_sqlalchemy import SQLAlchemy

import easyocr
import os
import pathlib
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import matplotlib.patches as patches
from markdown import markdown

app = Flask(__name__, static_folder='./static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ocr.db'
db = SQLAlchemy(app)

# create dir
img_dir = './static/img'
results_dir = './static/results'
os.makedirs(img_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

# setting
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/ocr',methods=['GET'])
def ocr():
    if request.method == 'GET':
        return render_template('ocr.html')
    else:
        file = request.files['img'] # ファイル取得
        file.save(os.path.join('static','img', file.filename)) # ファイル保存
        result = detect(file.filename)
        return render_template('result.html', filename=file.filename, result = result)
    

@app.route('/presentation',methods=['GET','POST'])
def presentation():
    if request.method == 'GET':
        # print(md.convert(sample_text))
        with open('./md/presentation.md', 'r', encoding='utf-8') as file:
            text = file.read()
        md = Markup(markdown(text))
        return render_template('md.html', md=md)

def detect(filename:str):
    """
    検出用関数
    """

    file_dir = os.path.join('static','img', filename)
    reader = easyocr.Reader(['en', 'ja'], gpu=False)
    result = reader.readtext(file_dir, detail=0)
    print(result)

    return result


if __name__ == "__main__":
    app.run(debug=True)