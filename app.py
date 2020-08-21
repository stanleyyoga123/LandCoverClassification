from flask import Flask, render_template, request, send_from_directory  
from werkzeug.utils import secure_filename
import os
from src import classifier

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
ESTIMATOR = 7
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = 'image.png'
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        classifier.run(os.path.join(UPLOAD_FOLDER, 'image.png'), ESTIMATOR)

        hists = os.listdir('static')
        return render_template('default.html', hists=hists) 
    else:
        return render_template('default.html')

@app.route('/', methods = ['GET'])
def main():
    return render_template('default.html')

@app.route('/uploader/<filename>')
def send_image(filename):
    return send_from_directory('static', filename)
		
if __name__ == '__main__':
   app.run(debug = True)