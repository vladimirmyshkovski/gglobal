from locust import HttpLocust, TaskSet

#def login(l):
#    l.client.post("/accounts/login", {"username":"pandabalu", "password":"pandabalu"})

def index(l):
    l.client.get("/")


#def admin(l):
#    l.client.get("/django-admin")

class UserBehavior(TaskSet):
    tasks = {index: 2}
    
    #def on_start(self):
    #    login(self)
	
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
