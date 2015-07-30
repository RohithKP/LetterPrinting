import os
from app import app
from flask import render_template,request, send_from_directory,url_for
import sec
import glob
import time
import random

root =  os.path.dirname(__file__)
path = os.path.join(root,'./static/odt/')
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
    print(i+' the value')
    r = int(i.encode('UTF8'))
    sec.renderx(templatename,int(i.encode('UTF8')),r)
    return render_template('out.html',templatename = str(r)+templatename)

@app.route('/sample/<templatename>')
def ren(templatename):
    return render_template('ren.html',temp=temp,templatename=templatename)

@app.route('/wodo/')
def wodo():
    tname = request.args.get('tname')
    wpath = os.path.join(root,'./templates/')
    return render_template('localeditor.html',tname=tname)
#    return send_from_directory(wpath, 'texteditor.html')
