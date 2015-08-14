import os
import json
from secretary import Renderer

def renderx(x,r,user):
    root =  os.path.dirname(__file__)
    base = os.path.join(root,'./static/users/'+user+'/')
    jdata = os.path.join(base,'./json/data.json')
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
    template = os.path.join(base, './odt/'+x)
# Configure custom application filters
    result = engine.render(template,address=addr )
    outf = os.path.join(base,'./out/')
    fname = os.path.join(outf,str(r)+x)
    output = open(fname, 'wb')
    output.write(result)
#for testing purpose
if __name__ == '__main__':
     renderx('test_template.odt')
