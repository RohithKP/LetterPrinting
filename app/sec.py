import os
import json
from secretary import Renderer
import requests

def renderx(x,n,user,projectname,jsonpath):
    root =  os.path.dirname(__file__)
    base = os.path.join(root,'./static/users/%s/%s/' %(user,projectname))
    jdata = os.path.join(base,'./json/data.json')
    try:
        r = requests.get(jsonpath)
    except requests.ConnectionError:
        return "Connection Error"
    rows_json = json.loads(r.text)
    print rows_json
    print n
    addr = rows_json[n]
    for key in addr: print key
    engine = Renderer()
    template = os.path.join(base, './odt/'+x)
# Configure custom application filters
    result = engine.render(template,address=addr )
    outf = os.path.join(base,'./out/')
    fname = os.path.join(outf,str(n)+x)
    output = open(fname, 'wb')
    output.write(result)
#for testing purpose
if __name__ == '__main__':
     renderx('test_template.odt')
