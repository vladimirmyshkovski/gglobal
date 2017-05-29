from django.contrib.sites.shortcuts import get_current_site 
from ipware.ip import get_real_ip, get_ip
from geolite2 import geolite2
from gglobal.crm.models import Form, Appeal, Assignment, Project
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from cities_light.models import City, Country
from gglobal.crm.models import PhoneNumber as Phone, Appeal, Leed, Form
from django.shortcuts import get_object_or_404, redirect
from river.models import State
from django.http.response import HttpResponse
from django.core.urlresolvers import reverse

# Create your views here.

@csrf_exempt
def CreateCRMApeal(request):
    if request.method == 'POST':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            print(request.POST.get('name'))
            print(request.POST.get('text'))
            print(request.POST.get('phone'))
            #Always use get on request.POST. Correct way of querying a QueryDict.
            ip = get_real_ip(request)
            reader = geolite2.reader()
            site = get_current_site(request)
            form, create = Form.objects.get_or_create(name=request.POST.get('form'))
            phone, phone_create = Phone.objects.get_or_create(phone_number=request.POST.get('phone'))
            if create:
                form.site = site
                form.save()

            if ip:
                CityByIP = reader.get(ip)['city']['names']['en']
                CountryByIP = reader.get(ip)['country']['names']['en']
            else:
                ip = get_ip(request)
                if ip:
                    try:
                        CityByIP = reader.get(ip)['city']['names']['en']
                        CountryByIP = reader.get(ip)['country']['names']['en']
                    except:
                        CityByIP = None
                        CountryByIP = None
            if CityByIP and CountryByIP is not None:
                try:
                    city = City.objects.get(name=CityByIP)
                    country = Country.objects.get(name=CountryByIP)
                    if not phone_create:
                        leed = Leed.objects.get(phone_number=phone)
                    leed = Leed(
                        name = request.POST.get('name'),
                        city = city,
                        site = site,
                        form = form,
                        text = request.POST.get('text')                        
                        )
                    leed.save()
                    leed.phone_number.add(phone)
                    leed.save()
                    appeal = Appeal(leed=leed)
                    appeal.save()
                except ObjectDoesNotExist:
                    pass
            if not phone_create:
                leed = Leed.objects.get(phone_number=phone)
            leed = Leed(
                name = request.POST.get('name'),
                site = site,
                form = form,
                text = request.POST.get('text')
                )
            leed.save()
            leed.phone_number.add(phone)
            leed.save()
            appeal = Appeal(leed=leed)
            appeal.save()
            #Returning same data back to browser.It is not possible with Normal submit
            return JsonResponse({'response': 200})
    #Get goes here
    return render(request,'base.html')



def proceed_appeal(request, appeal_id, next_state_id=None):
    appeal = get_object_or_404(Appeal, pk=appeal_id)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:
        appeal.proceed(request.user, next_state=next_state)
        if not appeal.owner:
            appeal.owner = request.user
            appeal.save()
        return redirect(reverse('admin:crm_appeal_changelist'))
    except Exception as e:
        return HttpResponse(e)


def proceed_appeal_single(request, appeal_id, next_state_id=None):
    appeal = get_object_or_404(Appeal, pk=appeal_id)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:
        appeal.proceed(request.user, next_state=next_state)
        if not appeal.owner:
            appeal.owner = request.user
            appeal.save()
        return redirect(reverse('admin:crm_appeal_change', args=[appeal_id]))
    except Exception as e:
        return HttpResponse(e)


def proceed_assignment(request, assignment_id, next_state_id=None):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:
        assignment.proceed(request.user, next_state=next_state)
        if not assignment.owner:
            assignment.owner = request.user
            assignment.save()

        if not assignment.get_available_proceedings(request.user):
            project = Project.objects.create(
                owner=request.user,
                assignment=assignment,
                )
            project.address.add(assignment.address)
            project.save()
        return redirect(reverse('admin:crm_assignment_changelist'))
    except Exception as e:
        return HttpResponse(e)


def proceed_assignment_single(request, assignment_id, next_state_id=None):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    next_state = get_object_or_404(State, pk=next_state_id)

    try:
        assignment.proceed(request.user, next_state=next_state)
        if not assignment.owner:
            assignment.owner = request.user
            assignment.save()

        if not assignment.get_available_proceedings(request.user):
            project = Project.objects.create(
                owner=request.user,
                assignment=assignment,
                )
            project.address.add(assignment.address)
            project.save()
        return redirect(reverse('admin:crm_assignment_change', args=[assignment_id]))
    except Exception as e:
        return HttpResponse(e)