import os
from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
import viewflow.nodes

from .models import ClientProcess,CRMUserProfile
from viewflow import frontend
from django.utils.translation import ugettext_lazy as _

#from gglobal.stream.activities import notification
from datetime import datetime

from notifications.signals import notify


#// "recipient" can also be a Group, the notification will be sent to all the Users in the Group
#notify.send(comment.user, recipient=group, verb=u'replied', action_object=comment,
#            description=comment.comment, target=comment.content_object)

#notify.send(follow_instance.user, recipient=follow_instance.follow_object, verb=u'has followed you',
#            action_object=instance, description=u'', target=follow_instance.follow_object, level='success')

from viewflow.decorators import flow_start_func
from notifications.signals import notify
from django.contrib.auth.models import User, Group

@flow_start_func
def create_flow(activation, **kwargs):
    data = kwargs['data']
    activation.process.form_name = data['name']
    activation.process.phone = data['phone']
    activation.prepare()
    activation.done()
    #notify.send(user, recipient=user, verb=u'Новая заявка!', action_object=user, description=user, target=user)
    return activation

@frontend.register
class ClientFlow(Flow):
    process_class = ClientProcess
    start = flow.StartFunction(create_flow).Next(this.approve)
    approve = (
        flow.View(
            UpdateProcessView,
            fields=["approved"]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.send)
        .Else(this.end)
    )

    send = (
        flow.Handler(
            this.send_hello_world_request
        ).Next(this.end)
    )

    end = flow.End()


    def send_hello_world_request(self, activation):
        from django.contrib.auth.models import User, Group
        masters = Group.objects.get(pk=1)
        user = User.objects.get(pk=1)

        #notify.send(user, recipient=user, verb='you reached level 10')
        notify.send(user, recipient=masters, verb=u'replied', action_object=user,
            description=user, target=user)
        print('youyouyou')






