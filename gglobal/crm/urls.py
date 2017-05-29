
from django.conf.urls import include, url
from gglobal.crm import views
urlpatterns = [
    url(
        regex=r'^~createclient/$',
        view=views.CreateCRMApeal,
        name='createclient'
        ),
    url(
    	regex=r'^proceed_appeal/(?P<appeal_id>\d+)/(?P<next_state_id>\d+)/$',
    	view=views.proceed_appeal,
    	name='proceed_appeal' ),
    url(
    	regex=r'^proceed_appeal_single/(?P<appeal_id>\d+)/(?P<next_state_id>\d+)/$',
    	view=views.proceed_appeal_single,
    	name='proceed_appeal_single' ),
    url(
    	regex=r'^proceed_assignment/(?P<assignment_id>\d+)/(?P<next_state_id>\d+)/$',
    	view=views.proceed_assignment,
    	name='proceed_assignment' ),
    url(
    	regex=r'^proceed_assignment_single/(?P<assignment_id>\d+)/(?P<next_state_id>\d+)/$',
    	view=views.proceed_assignment_single,
    	name='proceed_assignment_single' ),
]


