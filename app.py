from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import os
from src import classifier
import string
import random
import cv2
import importlib

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_filename():
    alphabet = string.ascii_letters
    ret = ''
    for i in range(10):
        ret += random.choice(alphabet)
    ret += '.png'
    return ret

def remove_files():
    path = os.listdir('static')
    for file in path:
        os.remove(os.path.join('static', file))

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        estimator = int(request.form.get('quantity'))
        f = request.files['file']
        filename = generate_filename()

        remove_files()
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        classifier.run(os.path.join(UPLOAD_FOLDER, filename), estimator)
        hists = [f'{filename[:-4]}_{i}.png' for i in range(estimator)]
        return redirect(url_for('combine_image'))
    else:
        return render_template('default.html')

@app.route('/result', methods = ['POST', 'GET'])
def combine_image():
    if request.method == 'POST':
        selected = request.form['data-arraySelected']
        selected = selected.split(',')
        selected_image = [int(el.split('_')[1]) for el in selected]

        image = classifier.combine(selected_image)
        filename = generate_filename()
        path = os.path.join('result', filename)
        cv2.imwrite(path, image)

        return redirect(url_for('final', filename=filename))
    else:
        return render_template('output.html', imp0rt = importlib.import_module)

@app.route('/combine/<filename>', methods = ['POST', 'GET'])
def final(filename):
    count = classifier.count_pix(os.path.join('result', filename))
    count = round(count/30)
    return render_template('finish.html', imp0rt = importlib.import_module, path=filename, count=count, hai='hehe')

@app.route('/result/<filename>')
def show_image(filename):
    return send_from_directory('result', filename)

@app.route('/static/<filename>')
def show_result(filename):
    return send_from_directory('static', filename)

@app.route('/logo/<filename>')
def im_utils(filename):
    return send_from_directory('logo', filename)
		
if __name__ == '__main__':
   app.run(debug = True)