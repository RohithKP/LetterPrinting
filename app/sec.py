import os
import json
from secretary import Renderer
import requests
import barcode
import random

def fnbarcode(barcod):
    ean = barcode.get('ean13',barcod)
    global imgpath
    imgpath = ean.save("/tmp/"+barcod)
    return imgpath

def renderx(x,user,projectname,data):
    root =  os.path.dirname(__file__)
    base = os.path.join(root,'./static/users/%s/%s/' %(user,projectname))
    jdata = os.path.join(base,'./json/data.json')
#     try:
#         r = requests.get(jsonpath)
#         addr = json.loads(r.text)
#     except :
#           return -1
    template = os.path.join(base, './odt/'+x)
    engine = Renderer()
    engine.environment.filters['fnbarcode'] = fnbarcode
    result = engine.render(template,data=data)
    outf = os.path.join(base,'./out/')
    templatename = str(random.uniform(0,100))+x
    fname = os.path.join(outf,templatename)
    data = []
    data.append(base)
    data.append(fname)
    data.append(templatename)
    output = open(fname, 'wb')
    output.write(result)
    return data

