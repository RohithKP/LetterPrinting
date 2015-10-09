import os
from app import app
from flask import render_template,request, send_from_directory,url_for,redirect,flash,session,g,flash
import sec
import glob
import time
import random,json
from werkzeug import secure_filename
from app import models,db
from flask_login import LoginManager,login_required, login_user, logout_user, current_user,current_app
from flask.ext.principal import identity_changed,Identity, Principal, Permission, RoleNeed, identity_loaded,UserNeed
import requests


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
    temp = os.listdir(os.path.join(root,'./static/users/%s/' % session['user_name']))
    print temp
    return render_template('dashboard.html',temp = temp)

@app.route('/try/',methods=['GET', 'POST'])
def tryit():
    templatename = request.form['templatename']
    jsonid = request.form['jsonid']
    jsonpath = request.form['jsonpath']+jsonid
    projectname = request.form['projectname']
    x = sec.renderx(templatename,session['user_name'],projectname,jsonpath)
    if x == -1:
       return 'error'
    else:   
       return render_template('out.html',templatename = templatename,projectname=projectname)

# render_template('out.html',templatename = templatename,projectname=projectname)

@app.route('/wodo/')
def wodo():
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
        filename =  request.form['tname']
        projectname =  request.form['projectname']
        os.path.join(os.path.join(root,'./static/users/%s/%s/odt/' % (session['user_name'],projectname)), filename)
        file.save(os.path.join(os.path.join(root,'./static/users/%s/%s/odt/' % (session['user_name'],projectname)), filename))
    return "saved"

@app.route('/signup/')
def signUp():
    return render_template('signup.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    username =  request.form['username'];
    password = request.form['password'];
    os.makedirs(path2+'/'+username)
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

@app.route('/preview',methods=['GET','POST'])
def preview():
    projectname =  request.args.get('projectname')
    print projectname
    filename = [f for f in os.listdir(path2+'/'+g.user.username+'/'+projectname+'/odt/') if f.endswith('.odt')]
    print filename[0]
    f = open(path2+'/'+g.user.username+'/'+projectname+'/url.txt', 'r')
    url = f.readline()
    jsonid = f.readline()
    try:
        r = requests.get(url+jsonid)
        addr = json.loads(r.text)
    except :
        flash('json cannot be loaded from the url')
        return render_template('preview.html',projectname=projectname,filename=filename[0],url=url,jsonid=jsonid)
   
    return render_template('preview.html',projectname=projectname,filename=filename[0],url=url,addr=addr,jsonid=jsonid)

         
        
@app.route('/createproject/', methods=['GET','POST'])
def create():
    projectname = request.form['projectname']
    url = request.form['url']
    os.makedirs(path2+'/'+g.user.username+'/'+projectname)
    os.makedirs(path2+'/'+g.user.username+'/'+projectname+'/odt')
    os.makedirs(path2+'/'+g.user.username+'/'+projectname+'/out')
    os.makedirs(path2+'/'+g.user.username+'/'+projectname+'/json')
    f = open(path2+'/'+g.user.username+'/'+projectname+'/url.txt', 'w')
    f.write(url)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.join(root,'./static/users/%s/%s/odt/' % (session['user_name'],projectname)), filename))
#         return redirect(url_for('preview',projectname=projectname,filename=filename))
        return redirect(url_for('index'))
    return 'Error creating project'


@app.route('/updateurl/', methods=['GET','POST'])
def updateurl():
    projectname = request.form['projectname']
    url = request.form['url']
    jsonid = request.form['jsonid']
    f = open(path2+'/'+g.user.username+'/'+projectname+'/url.txt', 'w')
    f.write(url+'\n')
    f.write(jsonid)
    return 'url updated'

