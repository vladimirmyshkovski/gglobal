import os
from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
import viewflow.nodes
from .models import ClientCRMProfile, AutoCreateClientProcess, AutoCreateProjectProcess
from viewflow import frontend
from django.utils.translation import ugettext_lazy as _
from cities_light.models import City, Country
#from gglobal.stream.activities import notification
from datetime import datetime
from django.conf import settings
from notifications.signals import notify
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib.sites.shortcuts import get_current_site 
from gglobal.users.models import User
from gglobal.crm.models import ClientCRMProfile
from django.contrib.auth.models import Group
from gglobal.crm.tasks import send_notifications_to_masters_by_city
from gglobal.crm.models import Project, PhoneNumber, CRMLeed, Complaint
from viewflow.decorators import flow_start_func
from notifications.signals import notify
import geocoder
from transliterate import translit
from django.contrib.sites.models import Site
from viewflow.models import Task
from gglobal.service.models import Service, Trouble

#// "recipient" can also be a Group, the notification will be sent to all the Users in the Group
#notify.send(comment.user, recipient=group, verb=u'replied', action_object=comment,
#            description=comment.comment, target=comment.content_object)

#notify.send(follow_instance.user, recipient=follow_instance.follow_object, verb=u'has followed you',
#            action_object=instance, description=u'', target=follow_instance.follow_object, level='success')



@flow_start_func
def auto_create_client_flow(activation, **kwargs):
    try:
        activation.process.city = kwargs['city']
    except:
        pass
    try:
        activation.process.country = kwargs['country']
    except:
        pass
    activation.process.form_name = kwargs['data']['form_name']
    activation.process.form_phone_number = kwargs['data']['phone_number']
    activation.process.creation_form = kwargs['data']['creation_form']

    activation.prepare()
    activation.done()
    #notify.send(user, recipient=user, verb=u'Новая заявка!', action_object=user, description=user, target=user)
    return activation

@flow_start_func
def auto_create_project_flow(activation, **kwargs):
    activation.prepare()
    activation.done()
    #notify.send(user, recipient=user, verb=u'Новая заявка!', action_object=user, description=user, target=user)
    return activation

@frontend.register
class AutoCreateClientFlow(Flow):
    process_title = 'Автоматическое создание клиента'
    process_description = 'Автоматическое создание клиента'
    process_class = AutoCreateClientProcess

    start = flow.StartFunction(
        auto_create_client_flow,
        task_title="Создана",
        task_description="Создана",
        ).Next(
        this.approve
        )

    approve = (
        flow.View(
            UpdateProcessView,
            task_title="Новая заявка",
            task_description="Принять заявку и созвониться",
            #task_result_summary='Получишь пизды, если не позвонишь!',
            fields=["approved"]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.select)
        .Else(this.approve)
    )

    select = (
        flow.View(
            UpdateProcessView,
            fields=["choices"],
        ).Next(
        this.switch
        )
    )

    switch = (
        flow.Switch()
        .Case(this.order, lambda activation: activation.process.choices == 'order')
        .Case(this.consultation, lambda activation: activation.process.choices == 'consultation')
        .Case(this.complaint, lambda activation: activation.process.choices == 'complaint')
    )

    consultation = (
        flow.View(
            UpdateProcessView,
            fields=["comment" ,"service", "trouble", "leed_city"]
        ).Permission(
            auto_create=True
        ).Next(
        this.create_leed
        )
    )

    complaint = (
        flow.View(
            UpdateProcessView,
            fields=["complaint_troube", "complaint_project_id"]
        ).Permission(
            auto_create=True
        ).Next(
        this.create_complaint
        )
    )

    order = (
        flow.View(
            UpdateProcessView,
            task_title="Новый заказ",
            task_description="Создание нового заказа",
            fields=[
            "first_name", "last_name", "phone_number1", 
            "phone_number2", "phone_number3", "phone_number4", 
            "phone_number5", "comment", "service","trouble","address",
            ]
        ).Permission(
            auto_create=True
        ).Next(this.create_order)
    )

    create_order = (
        flow.Handler(
            this.send_notification_about_create_order_request
        ).Next(this.end)
    )

    create_leed = (
        flow.Handler(
            this.just_create_leed
        ).Next(this.end)
    )

    create_complaint = (
        flow.Handler(
            this.send_notification_about_create_complaint_request
        ).Next(this.end)
    )

    end = flow.End()

    def send_notification_about_create_complaint_request(self, activation):
        complaint, create = Complaint.objects.get_or_create(
            trouble=activation.process.complaint_troube,
            project=activation.process.complaint_project_id,
            )


    def just_create_leed(self, activation):
        leed, create = CRMLeed.objects.get_or_create(
            comment=activation.process.comment,
            city=activation.process.leed_city,
            name=activation.process.form_name,
            )
        phone, create = PhoneNumber.objects.get_or_create(phone_number=activation.process.form_phone_number)
        #print(activation.process.service)
        #leed.trouble.add(activation.process.trouble)
        #leed.service.add(activation.process.service)


    def send_notification_about_create_order_request(self, activation):
        phone_numbers = [
        activation.process.phone_number1,
        activation.process.phone_number2,
        activation.process.phone_number3,
        activation.process.phone_number4,
        activation.process.phone_number5,
        ]
        user_data = {
        'first_name'    :   activation.process.first_name,
        'last_name'     :   activation.process.last_name,
        }

        g = geocoder.google([
        activation.process.address.latitude, 
        activation.process.address.longitude
        ],
        method='reverse',
        key=settings.GOOGLE_MAP_API_KEY
        )
        try:
            city = City.objects.get(name=g.city)
        except ObjectDoesNotExist:
            city = None
        try:
            country = Country.objects.get(name=g.country_long)
        except ObjectDoesNotExist:
            country = None

        project_data = {
        'comment'       : activation.process.comment,
        'service'       : activation.process.service,
        'trouble'       : activation.process.trouble,
        }

        location_data = {
        'city'          :   city,
        'country'       :   country,
        'site'          :   activation.process.sites,
        'address'       :   activation.process.address,
        }
        username = translit(("{}{}").format(user_data['first_name'], user_data['last_name']), "ru", reversed=True)
        user, create = User.objects.get_or_create(
            username = username, 
            first_name = user_data['first_name'],
            last_name = user_data['last_name'],
            country = location_data['country'],
            position = location_data['address'],
            )
        for phone_number in phone_numbers:
            if not phone_number == '':
                phone, create = PhoneNumber.objects.get_or_create(phone_number=phone_number)        
            user.phone_number.add(phone)
        site = Site.objects.get(pk=1) # <------ FIX THIX
        user.cities.add(location_data['city'])
        user.sites.add(site) # <------ FIX THIX
        user.save()
        client, create = ClientCRMProfile.objects.get_or_create(
            user=user)
        print(client)
        process_owner_id = Task.objects.filter(process_id=activation.process.id, owner_permission__isnull=False).latest('created')
        created_by = User.objects.get(pk=process_owner_id.owner_id)
        project = Project(
            client=client,
            created_by=created_by,
            address=location_data['address'],
            site=site,
            contact_phone_number=activation.process.phone_number1,
            )
        project.save()
        AutoCreateProjectFlow.start.run()
        #masters = User.objects.filter(mastercrmprofile__isnull=False, city=data['city'])
        #send_notifications_to_masters_by_city(masters)

        #notify.send(user, recipient=user, verb=u'replied', action_object=user,
        #    description=user, target=user)
        


@frontend.register
class AutoCreateProjectFlow(Flow):
    process_class = AutoCreateProjectProcess

    start = flow.StartFunction(
        auto_create_client_flow,
        task_title="Создана",
        task_description="Создана",
        ).Next(
        this.approve
        )

    approve = (
        flow.View(
            UpdateProcessView,
            task_title="Новая заявка",
            task_description="Принять заказ и созвониться",
            #task_result_summary='Получишь пизды, если не позвонишь!',
            fields=["approved"]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.end)
        .Else(this.approve)
    )

    end = flow.End()
