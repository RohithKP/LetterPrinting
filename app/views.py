import os
from app import app
from flask import render_template,request, send_from_directory,url_for,redirect,flash,session
import sec
import glob
import time
import random,json
from werkzeug import secure_filename
from app import models,db

root =  os.path.dirname(__file__)
path = os.path.join(root,'./static/odt/')
path2 = os.path.join(root,'./static/save/')

UPLOAD_FOLDER = path
ALLOWED_EXTENSIONS = set(['odt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'some_secret'
#temp = glob.glob(path)


@app.route('/')
@app.route('/index')
def index():
    temp = os.listdir(path)
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
     global tname
     tname = request.args.get('tname')
     return render_template('localeditor.html',tname=tname)
  #  return send_from_directory(wpath, 'texteditor.html')

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
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/save/',methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        file = request.files['data']
        print(tname)
        file.save(os.path.join(path, tname[1:]))
        return redirect(url_for('index'))

@app.route('/signup/')
def signUp():
    flash('Logged in successfully.')
    return render_template('signup.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    u = models.User(nickname=user, password=password)
    db.session.add(u)
    db.session.commit()
    users = models.User.query.all()
    for u in users:
        print(u.id,u.nickname)
    return json.dumps({'status':'OK','user':user,'pass':password});

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
          if request.form['password'] == 'password' and request.form['username'] == 'admin':
              session['logged_in'] = True
          else:
              flash('wrong password!')
          return index()
    else:
       return render_template('login.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
