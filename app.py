from flask import Flask, render_template, request, send_from_directory  
from werkzeug.utils import secure_filename
import os
from src import classifier

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        estimator = int(request.form.get('quantity'))
        f = request.files['file']
        filename = 'image.png'
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        classifier.run(os.path.join(UPLOAD_FOLDER, 'image.png'), estimator)

        hists = os.listdir('static')
        return render_template('default.html', hists=hists) 
    else:
        return render_template('default.html')

@app.route('/', methods = ['GET'])
def main():
    import importlib
    return render_template('output.html', imp0rt = importlib.import_module)

@app.route('/uploader/<filename>')
def send_image(filename):
    return send_from_directory('static', filename)
		
if __name__ == '__main__':
   app.run(debug = True)