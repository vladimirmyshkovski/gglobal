from river.handlers.completed import PostCompletedHandler
from .models import Assignment




def handler(Assignment,field='status',*args,**kwargs):
    print('asdasd')

PostCompletedHandler.register(handler,Assignment,'status')