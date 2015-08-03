import os
import json
from secretary import Renderer

def renderx(x,r,path):
    root =  os.path.dirname(__file__)
    jdata = os.path.join(root,'./static/json/'+path+'.json')
    with open(jdata) as data_file:
         address = json.load(data_file)
    n = r
#    i = 0;
#    for a in address['address']:
	#pprint(address['address'][i])
    addr = address['address'][n]
#        i+=1
    print(addr)
    engine = Renderer()
    template = os.path.join(root, './static/odt/'+x)
# Configure custom application filters
    result = engine.render(template,address=addr )
    outf = os.path.join(root,'./static/out')
    fname = os.path.join(outf,str(r)+x)
    output = open(fname, 'wb')
    output.write(result)
#for testing purpose
if __name__ == '__main__':
     renderx('test_template.odt')
