from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from gglobal.crm.flows import ClientFlow

@csrf_exempt
def СreateClientView(request):
    if request.method == 'POST':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            #Always use get on request.POST. Correct way of querying a QueryDict.
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            data = {"name": name , "phone" : phone}
            #ClientFlow.start.run(data=data)
            #Returning same data back to browser.It is not possible with Normal submit
            return JsonResponse(data)
    #Get goes here
    return render(request,'base.html')
