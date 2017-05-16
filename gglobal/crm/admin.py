from django.contrib import admin
from gglobal.crm.models import ClientCRMProfile, MasterCRMProfile, Invoice, \
								Status, Activity, Project, PaymentMethod, \
								PaymentType, CRMLeed, PhoneNumber
from allauth.account.utils import send_email_confirmation
from gglobal.users.models import User


# Register your models here.
#admin.site.register(MasterCRMProfile)




admin.site.register(ClientCRMProfile)
admin.site.register(CRMLeed)
admin.site.register(Invoice)
admin.site.register(Status)
admin.site.register(Activity)
admin.site.register(Project)
admin.site.register(PaymentMethod)
admin.site.register(PaymentType)
admin.site.register(PhoneNumber)



'''
MasterAdmin
    def get_queryset(self, request):
        qs = super(MyModelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
'''












def send_email_confirm(modeladmin, request, queryset):
    for master in queryset:
        user = User.objects.get(pk=master.user.pk)
        send_email_confirmation(request, user, signup=False)
        print('sended')

send_email_confirm.short_description = 'Отправить письмо с подтверждением электронной почты'

class MasterAdmin(admin.ModelAdmin):
    actions = [send_email_confirm, ]  # <-- Add the list action function here


admin.site.register(MasterCRMProfile, MasterAdmin)

from controlcenter import Dashboard, widgets
from controlcenter import app_settings

class ModelItemList(widgets.ItemList):
    model = MasterCRMProfile
    list_display = [app_settings.SHARP, 'pk', 'user']
    list_display_links = ['user']
    limit_to = 50
    height = 300
    sortable = True


    '''
    def get_queryset(self):
        restaurant = super(MenuWidget, self).get_queryset().get()
        today = timezone.now().date()
        return (restaurant.menu
                          .filter(orders__created__gte=today, name='ciao')
                          .order_by('-ocount')
                          .annotate(ocount=Count('orders')))
	'''





class BestMastersSingleBarChart(widgets.SingleBarChart):
    title = 'Лучшие мастера'
    model = MasterCRMProfile

    class Chartist:
        options = {
            # Displays only integer values on y-axis
            'onlyInteger': True,
            # Visual tuning
            'chartPadding': {
                'top': 24,
                'right': 0,
                'bottom': 0,
                'left': 0,
            }
        }

    def legend(self):
        # Duplicates series in legend, because Chartist.js
        # doesn't display values on bars
        return self.series

    def values(self):
        # Returns pairs of restaurant names and order count.
        queryset = self.get_queryset()
        return (queryset.values_list('pk'))



class MyDashboard(Dashboard):
	title = 'Мастера'
	widgets = (
		widgets.Group(
			[ModelItemList],
			width=widgets.LARGER, height=300
		)
	)













