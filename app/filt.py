from secretary import Renderer
import barcode
import os
root =  os.path.dirname(__file__)
temp = os.path.join(root,'./static/test_template2.odt')
imgpath = ""
engine = Renderer()
# Configure custom application filters
def square(barcod):
    ean = barcode.get('ean13',barcod)
    global imgpath
    imgpath = ean.save('image')

# if imgpath:
#     print 'imgpath'-imgpath
#     engine.environment.filters['square'] = square
#     result = engine.render(temp,x=imgpath)
#     output = open('rendered_document.odt', 'wb')
#     output.write(result)

# import os
# import json
# from secretary import Renderer
# import requests
# import barcode
# from barcode.writer import ImageWriter

# def fnbarcode(barcod):
#     ean = barcode.get('ean13',barcod)
#     global imgpath
#     imgpath = ean.save('image')
#     return imgpath

# def renderx(x,user,projectname,jsonpath):
#     root =  os.path.dirname(__file__)
#     base = os.path.join(root,'./static/users/%s/%s/' %(user,projectname))
#     jdata = os.path.join(base,'./json/data.json')
#     try:
#         r = requests.get(jsonpath)
#     except requests.ConnectionError:
#         return "Connection Error"
#     addr = json.loads(r.text)
#     barcod = addr[0]["clm_no"]
#     image = os.path.join(root, './static/barcodes/'+barcod)
#     ean = barcode.get('ean13',barcod)
#     imgpath = ean.save(image)
#     template = os.path.join(base, './odt/'+x)
#     engine = Renderer()
#     engine.environment.filters['fnbarcode'] = fnbarcode
#     result = engine.render(template,data=addr,image=imgpath)
#     outf = os.path.join(base,'./out/')
#     fname = os.path.join(outf,x)
#     output = open(fname, 'wb')
#     output.write(result)
