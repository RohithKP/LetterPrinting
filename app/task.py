from celery import Celery
from app import app
from celery.task import Task
import sec
from subprocess import Popen,PIPE
# from flask import session,current_app
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

@celery_app.task(name='generate',queue='genq')
def generate(templatename,jsonpath,projectname,user,arr=[] ):
     print 'generate task was called'
     ti = user
     for i in range(arr[0],arr[1]+1):
           render.delay(templatename,jsonpath+str(i),projectname,user)
           ti= counter()
           ti.delay(user,projectname)

@celery_app.task(name='render',queue='renq')
def render(templatename,jsonpath,projectname,user):
         odtout =  sec.renderx(templatename,user,projectname,jsonpath)
         print odtout
         pdfgen.delay(odtout)

@celery_app.task(name='pdfgen',queue='pdfq')
def pdfgen(odtout):
    print 'inside pdfgen'
    p = Popen('unoconv --format pdf --output '+odtout[0]+'pdfs/'+odtout[2]+'.pdf'+' '+str(odtout[1]),shell=True,stdout=PIPE,stderr=PIPE)
    err = p.communicate()
#     if err != "('', '')":
    print err


class counter(Task):
    queue = "countq"
    taskCount = 0;
    print "inside cpunter"
    def __call__(self, *args, **kwargs):
        """In celery task this function call the run method, here you can
        set some environment variable before the run of the task"""
        print "haiiiii"
        counter.taskCount += 1
        print counter.taskCount
        return self.run(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        #exit point of the task whatever is the state
        pass

    def run(self, *args, **kwargs):
        print "inside run****************"
        print args[0]
        print args[1]
        if counter.taskCount == 5 :
           print "data base is updated"
           counter.taskCount = 0
        else :
           print "yet to go"
