from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# import easyocr
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ocr.db'
db = SQLAlchemy(app)

# create dir
img_dir = './static/img'
results_dir = './static/results'
os.makedirs(img_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return redirect('/')

@app.route('/ocr',methods=['GET','POST'])
def ocr():
    if request.method == 'GET':
        return render_template('ocr.html')
    else:
        # reader = easyocr.Reader(['en', 'ja'], gpu=True)
        # result = reader.readtext('japanese.jpg', detail=0)
        # print(result)
        file = request.files['img'] # ファイル取得
        file.save(os.path.join('./static/img', file.filename)) # ファイル保存

        return render_template('result.html', filename=file.filename)

if __name__ == "__main__":
    app.run(debug=True)