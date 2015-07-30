import os
import json
from secretary import Renderer

def renderx(x,i):
    root =  os.path.dirname(__file__)
    jdata = os.path.join(root,'./static/data.json')
    with open(jdata) as data_file:
         address = json.load(data_file)

#    i = 0;
#    for a in address['address']:
	#pprint(address['address'][i])
    addr = address['address'][i]
#        i+=1
    engine = Renderer()
    template = os.path.join(root, './static/odt/'+x)
# Configure custom application filters
    result = engine.render(template,address=addr )

    outf = os.path.join(root,'./static/out')
    fname = os.path.join(outf,x+'.odt')
    output = open(fname, 'wb')
    output.write(result)
#for testing purpose
if __name__ == '__main__':
     renderx('test_template.odt')
