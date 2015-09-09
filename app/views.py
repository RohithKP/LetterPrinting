import os
from app import app
from flask import render_template,request, send_from_directory,url_for,redirect,flash,session,g
import sec
import glob
import time
import random,json
from werkzeug import secure_filename
from app import models,db
from flask_login import LoginManager,login_required, login_user, logout_user, current_user,current_app
from flask.ext.principal import identity_changed,Identity, Principal, Permission, RoleNeed, identity_loaded,UserNeed

root =  os.path.dirname(__file__)
path2 = os.path.join(root,'./static/users/')
ALLOWED_EXTENSIONS = set(['odt'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'some_secret'

# flask-login
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "login"
login_manager.init_app(app)
#flask principal
principal =Principal()
admin_permission= Permission(RoleNeed('admin'))
principal.init_app(app)
user = None


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
       g.user = models.User.query.get(session['user_id'])

@app.route('/')
@app.route('/index')
@login_required
def index():
    temp = os.listdir(os.path.join(root,'./static/users/%s/odt/' % session['user_name']))
    return render_template('index.html',temp = temp)

@app.route('/gen/')
#@app.route('/gen/<templatename>')
def gen():
    templatename = request.args.get('templatename')
    i = request.args.get('jsonid')
    jpath = request.args.get('jsonpath')
    r = int(i.encode('UTF8'))
    sec.renderx(templatename,r,session['user_name'])
    return render_template('out.html',templatename = str(r)+templatename)

#@app.route('/sample/<templatename>')
#def ren(templatename):
#    return render_template('ren.html',temp=temp,templatename=templatename)

@app.route('/wodo/')
def wodo():
     global tname
     tname = request.args.get('tname')
     return render_template('localeditor.html')
  #  return send_from_directory(wpath, 'texteditor.html')

@app.route('/ViewerJS/')
def viewer():
    wpath = os.path.join(root,'./static/ViewerJS/')
    return send_from_directory(wpath,'index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.path.join(root,'./static/users/%s/odt/' % session['user_name']), filename))
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
    return send_from_directory(os.path.join(root,'./static/users/%s/odt/' % session['user_name']), filename)

@app.route('/save/',methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        file = request.files['data']
        file.save(os.path.join(os.path.join(root,'./static/users/%s/odt/' % session['user_name']), tname))
        return redirect(url_for('index'))

@app.route('/signup/')
def signUp():
    return render_template('signup.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    username =  request.form['username'];
    password = request.form['password'];
    os.makedirs(path2+'/'+username)
    os.makedirs(path2+'/'+username+'/odt')
    os.makedirs(path2+'/'+username+'/out')
    os.makedirs(path2+'/'+username+'/json')
    user = models.User(username=username, password=password)
    db.session.add(u)
    db.session.commit()
    session['logged_in'] = True
    session['user_id'] = user.id
    session['user_name'] = user.username
    login_user(user)
    users = models.User.query.all()
    for u in users:
        print(u.id,u.username)
    return redirect(url_for('login'))
@app.route('/login', methods=['GET','POST'])
def login():
       return render_template('login.html')
@app.route('/check', methods=['GET','POST'])
def check():
    POST_USERNAME = request.form['username']
    POST_PASSWORD = request.form['password']
    print request.args.get('username')
    if models.User.query.filter_by(username=POST_USERNAME,password=POST_PASSWORD).first():
       global user
       user = models.User.query.filter_by(username=POST_USERNAME,password=POST_PASSWORD).first()
       session['logged_in'] = True
       session['user_name'] = user.username
       session['user_id'] = user.id
       #render_template('index.html',)
       login_user(user)
       identity_changed.send(current_app._get_current_object(),identity=Identity(user.id))
       global path1
       path1 = os.path.join(root,'./static/users/%s/odt/' % session['user_name'])
       return redirect(url_for('index'))
    else:
       flash('wrong password!')
       return redirect(url_for('login'))
    return redirect(url_for('index'))
@app.route("/logout")
@login_required
def logout():
    session['logged_in'] = False
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
        return models.User()

@app.route('/admin',methods=['GET'])
@admin_permission.require(http_exception=403)
def admin():
    return render_template('admin.html')

@app.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return render_template('denied.html')

@identity_loaded.connect_via(app)
def on_identity_loaded(sender,identity):
    identity.user = user
    print "efe"
    if hasattr(user,'id'):
       print user.id
       identity.provides.add(UserNeed(user.id))

    if hasattr(user,'roles'):
       for role in user.roles:
           print role.name
           identity.provides.add(RoleNeed(role.name))
