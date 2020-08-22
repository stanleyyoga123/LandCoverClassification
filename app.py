from flask import Flask, render_template, request, send_from_directory  
from werkzeug.utils import secure_filename
import os
from src import classifier
import string
import random

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
ESTIMATOR = 7
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

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = generate_filename()

        remove_files()
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        classifier.run(os.path.join(UPLOAD_FOLDER, filename), ESTIMATOR)

        hists = [f'{filename[:-4]}_{i}.png' for i in range(ESTIMATOR)]
        return render_template('default.html', hists=hists) 
    else:
        return render_template('default.html')

@app.route('/', methods = ['GET'])
def main():
    import importlib
    return render_template('output.html', imp0rt = importlib.import_module)
		
if __name__ == '__main__':
   app.run(debug = True)