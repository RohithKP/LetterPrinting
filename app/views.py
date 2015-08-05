import os
from app import app
from flask import render_template,request, send_from_directory,url_for,redirect
import sec
import glob
import time
import random
from werkzeug import secure_filename

root =  os.path.dirname(__file__)
path = os.path.join(root,'./static/odt/')
path2 = os.path.join(root,'./static/save/')

UPLOAD_FOLDER = path
ALLOWED_EXTENSIONS = set(['odt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#temp = glob.glob(path)
temp = os.listdir(path)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',temp = temp)

@app.route('/gen/')
#@app.route('/gen/<templatename>')
def gen():
    templatename = request.args.get('templatename')
    i = request.args.get('jsonid')
    path = request.args.get('jsonpath')
    r = int(i.encode('UTF8'))
    sec.renderx(templatename,r,str(path))
    return render_template('out.html',templatename = str(r)+templatename)

#@app.route('/sample/<templatename>')
#def ren(templatename):
#    return render_template('ren.html',temp=temp,templatename=templatename)

@app.route('/wodo/')
def wodo():
    tname = request.args.get('tname')
  #  wpath = os.path.join(root,'./templates/')
    return render_template('localeditor.html',tname=tname)
#    return send_from_directory(wpath, 'texteditor.html')

@app.route('/ViewerJS/')
def viewer():
    wpath = os.path.join(root,'./static/ViewerJS/')
    return send_from_directory(wpath,'index.html')

@app.route('/temp/')
def func():
    return render_template('vjs.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/save/',methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        file = request.files['data']
        filename = request.args.get('name')
        file.save(os.path.join(path2, ''+str(random.randint(3, 99))))
        return redirect(url_for('index'))
