from django.shortcuts import render
from django.template import RequestContext
from gglobal.service.models import Service
# Create your views here.

def show_services(request):
	return render(request, "service/index.html", {'nodes':Service.objects.all()})

