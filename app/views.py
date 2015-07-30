import os
from app import app
from flask import render_template,request
import sec
import glob

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
    sec.renderx(templatename,1)
    return render_template('out.html',templatename = templatename)

@app.route('/sample/<templatename>')
def ren(templatename):
    return render_template('ren.html',temp=temp,templatename=templatename)
