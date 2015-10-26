from celery import Celery
from app import app
from celery.task import Task
import sec
from subprocess import Popen,PIPE
import os
import os.path
import random
import requests
import json
from billiard import current_process

"""
check : Batch processing of pdfs
"""
def make_celery(app):
    celery = Celery(app.import_name, broker='amqp://')
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
celery_app = make_celery(app)

@celery_app.task(name='generate',queue='genQ')
def generate(templatename,jsonpath,projectname,user,arr=[]):
      print 'generate task was called'
      print str(current_process().index) +"aadad"
      uri="http://localhost:4000/fetchRange/"
      data = {"start":arr[0], "end":arr[1]}
      print data
      headers = {'Content-Type': 'application/json'}
      payload = json.dumps(data)
      try:
          r = requests.post(uri, data=payload,headers=headers)
          jsonrows= json.loads(r.text)
      except:
          print 'error fetching json'
      for i in range(arr[0],arr[1]):
          print i
          render.delay(templatename,json.loads(jsonrows[str(i)]),projectname,user)

@celery_app.task(name='render',queue='renQ')
def render(templatename,data,projectname,user):
         print "render was called"+str(current_process().index)
         odtout =  sec.renderx(templatename,user,projectname,data)
         if os.path.isfile(str(odtout[1])):
              pdfgen.delay(odtout,user,projectname)

@celery_app.task(name='pdfgen',queue='pdfqu')
def pdfgen(odtout,user,projectname):
      print 'inside pdf gen'+str(odtout[1])
      while True:
           p = Popen('unoconv --format pdf -p 222'+str(current_process().index)+' --output '+str(odtout[0])+'pdfs/'+str(odtout[2])+'.pdf '+' '+str(odtout[1]),shell=True,stdout=PIPE,stderr=PIPE)
           err = p.communicate()
           print 'asdas'
           if str(err) == "('', '')" :
               print "success"
               break
           else :
               print str(err)+'error'
               break










# class counter(Task):
#     queue = "countq"
#     taskCount = {}
#     path = '/home/taiga/Documents/Templating/app/./static/users/'
#     print "inside cpunter"
#     def __call__(self, *args, **kwargs):
#         """In celery task this function call the run method, here you can
#         set some environment variable before the run of the task"""
#         print args[0]+args[1]
#         if not args[0]+args[1] in counter.taskCount:
#             counter.taskCount[args[0]+args[1]] = 0
#         else:
#             counter.taskCount[args[0]+args[1]] += 1

#         print counter.taskCount[args[0]+args[1]]
#         return self.run(*args, **kwargs)

#     def after_return(self, status, retval, task_id, args, kwargs, einfo):
#         #exit point of the task whatever is the state
#         pass

#     def run(self, *args, **kwargs):
#         print "inside run****************"
#         if counter.taskCount[args[0]+args[1]]%10 == 0 :
#            f = open(counter.path+args[0]+'/'+args[1]+'/count.txt', 'wb')
#            f.write(str(counter.taskCount[args[0]+args[1]]))
#            print "data base is updated"
#         else :
#            print "yet to go"
