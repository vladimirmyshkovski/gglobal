from django.contrib import admin
from allauth.account.utils import send_email_confirmation
from gglobal.users.models import User
from django.db import models
from django.utils.translation import ugettext as _
from gglobal.crm.forms import ActivityForm, ClientForm, ComplaintForm, SalaryForm
from django.conf.urls import url
#from django_object_actions import DjangoObjectActions
#from django_admin_row_actions import AdminRowActionsMixin
#from inline_actions.admin import InlineActionsMixin
#from inline_actions.admin import InlineActionsModelAdminMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from gglobal.cms.models import ExecutantProfilePage, ExecutantIndexPage
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from functools import WRAPPER_ASSIGNMENTS, update_wrapper, wraps
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from jet.admin import CompactInline
from jet.filters import RelatedFieldAjaxListFilter
#from admin_utils.mixins import FoldableListFilterAdminMixin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Avg
from django.contrib.admin.views.main import ChangeList
from .admin_buttons import assignment_passing_button, telegram_auth_button
from gglobal.crm.models import ClientProfile, ExecutantProfile, Invoice, \
                                Activity, Project, Payment, \
                                Card, Leed, Appeal, Source, \
                                Assignment, PhoneNumber, Complaint, \
                                Address, PriceList, Price, Salary, Bonus
#from river.services.state import StateService
from django.contrib.contenttypes.models import ContentType
from .utils import username_generator
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from fsm_admin.mixins import FSMTransitionMixin
from gglobal.users.models import User
from django.db.models import Q
from django.contrib.admin.utils import flatten_fieldsets
from django import forms
from gglobal.tmb.models import User as TelegramUser

admin.site.site_header = 'Monty Python administration'
admin.site.site_title = 'Monty Python administration'
admin.site.index_title = 'Monty Python administration'


class BaseAdmin(admin.ModelAdmin):
    class Media:
        js = ("/static/js/admin/instantsearch.js",)


#################
# INLINES ADMIN #

class InlineExecutantProfileAdmin(admin.StackedInline):
    model = ExecutantProfile
    extra = 1
    can_delete = False
    verbose_name_plural = 'Мастер'
    fk_name = 'user'


class InlineClientProfileAdmin(admin.StackedInline):
    model = ClientProfile
    extra = 1
    can_delete = False
    verbose_name_plural = 'Клиент'
    fk_name = 'user'


class InlineAssigmentAdmin(CompactInline):
    model = Assignment
    max_num = 1
    #min_num = 0
    extra = 1
    readonly_fields = ['state']
    
    def get_fields(self, request, obj):
        if obj:
            if request.user.groups.filter(name='Managers').exists():
                return ['type', 'client', 'appeal', 'date', 'address']
        return super(InlineAssigmentAdmin, self).get_fields(request, obj)


class InlineComplaintAdmin(CompactInline):
    model = Complaint
    max_num = 1
    #min_num = 0
    extra = 1

    def get_fields(self, request, obj):
        if obj:
            if not request.user.is_superuser:
                return ['project']
        return super(InlineComplaintAdmin, self).get_fields(request, obj)

class InlineActivityAdmin(GenericStackedInline):
    model = Activity
    form = ActivityForm
    extra = 1

class InlinePhoneNumberAdmin(CompactInline):
    model = PhoneNumber
    extra = 1

    def get_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['phone_number']
        return super(InlinePhoneNumberAdmin, self).get_fields(request, obj)

class InlineInvoiceAdmin(CompactInline):
    show_change_link = True
    model = Invoice
    extra = 1
    readonly_fields = ['state']

    def get_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['state', 'amount']
        return super(InlineInvoiceAdmin, self).get_fields(request, obj)

    def get_readonly_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['amount', 'state']
        return super(InlineInvoiceAdmin, self).get_readonly_fields(request, obj)


class InlinePriceListAdmin(CompactInline):
    model = PriceList
    extra = 1

    def get_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['service', 'trouble', 'time', 'from_price', 'to_price', 'above_price']
        return super(InlinePriceListAdmin, self).get_fields(request, obj)


class InlinePriceAdmin(admin.StackedInline):
    show_change_link = True
    model = Price
    extra = 1

    def get_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['service', 'trouble', 'price', 'time']
        return super(InlinePriceAdmin, self).get_fields(request, obj)

# END INLINES ADMIN #
#####################

@admin.register(Appeal)
class AppealAdmin(FSMTransitionMixin, BaseAdmin):
    change_form_template = 'admin/fsm-transition/change_form.html'
    search_fields = ['id', '@leed__phone_number__phone_number']
    list_display = ['pk', 'state', 'source', 'phone_number']
    list_select_related = True
    list_filter = ('source', 'state')
    list_select_related = True
    preserve_filters = True
    readonly_fields = ('state', 'phone_number')

    
    inlines = [
        InlineAssigmentAdmin,
        InlineComplaintAdmin,
        InlineActivityAdmin
    ]
    can_delete = False
    
    def phone_number(self, obj):
        if not obj.state == 'new':
            return ', '.join([ i.phone_number for i in obj.leed.phone_number.all()[:5] ])

            #return PhoneNumber.objects.filter(content_object=obj.leed).first()
        else:
            return None
    phone_number.short_description = 'Номера телефона лида'
    phone_number.empty_value_display = 'Сначала нужно принять обращение'
    
    '''
    def get_fieldset(self, request, obj):
        if obj:
            if not request.user.is_superuser:
                if obj.state == 'new' or obj.state == 'handed':

        return super(AppealAdmin, self).get_fieldset(request, obj)
    '''

    def get_fields(self, request, obj):
        if obj:
            if not request.user.is_superuser:
                if obj.state == 'new' or obj.state == 'handed':
                    return ['state']
                else:
                    return ['leed', 'phone_number', 'text', 'state', 'source', 'trouble', 'service', 'city']
        else:
            if not request.user.is_superuser:
                return ['leed', 'text', 'state', 'source', 'trouble', 'service', 'city']
        return super(AppealAdmin, self).get_fields(request, obj)
    
    def get_inline_instances(self, request, obj):
        if obj:
            if not request.user.is_superuser:
                print(obj.state)
                if obj.state == 'new' or obj.state == 'handed':
                    return []
        else:
            if not request.user.is_superuser:
                return []                        
        return super(AppealAdmin, self).get_inline_instances(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False
    
@admin.register(Assignment)
class AssignmentAdmin(FSMTransitionMixin, BaseAdmin):
    list_display = ['pk', 'type', 'state', 'date', 'address', 'passing_action']
    list_filter = ('date', 'type', 'state')
    preserve_filters = True
    inlines = [InlineActivityAdmin]
    readonly_fields = ('state', )

    #def time_seconds(self, obj):
    #    if obj.date:
    #        return obj.date.strftime("%d %b %Y %H:%M:%S")
    #time_seconds.short_description = 'Дата и время заявки'
    #time_seconds.empty_value_display =  'Время не было указано'
    
    def get_queryset(self, request):
        qs = super(AssignmentAdmin, self).get_queryset(request)
        if request.user.is_superuser or not request.user.groups.filter(name='Masters').exists():
            return qs
        master = ExecutantProfile.objects.get(user=request.user)
        return qs.filter(Q(address__city__in=master.work_cities.all(), owner__isnull=True, appeal__state='handed') |\
                         Q(address__city__in=master.work_cities.all(), owner=master, appeal__state='handed'))\
                        .exclude(passing_masters__in=[master])

    def get_readonly_fields(self, request, obj):
        if obj:
            if request.user.groups.filter(name='Masters').exists():
                return ['type', 'state', 'client', 'trouble', 'service', 'appeal', 'date', 'address']
        return super(AssignmentAdmin, self).get_readonly_fields(request, obj)

    def get_list_display(self, request):
        self.user = request.user
        self.executant = ExecutantProfile.objects.filter(user=self.user).exists()
        return super(AssignmentAdmin, self).get_list_display(request)

    def get_fields(self, request, obj):
        if obj:
            #if request.user.groups.filter(name='Masters').exists():
            if not request.user.is_superuser:
                return ['type', 'state', 'client', 'trouble', 'service', 'appeal', 'date', 'address']
        else:
            if not request.user.is_superuser:
                return ['type', 'state', 'client', 'trouble', 'service', 'appeal', 'date', 'address']
        return super(AssignmentAdmin, self).get_fields(request, obj)

    def passing_action(self, obj):
        content = ""
        if self.executant and self.user.groups.filter(name='Masters').exists():
            executants = Assignment.objects.filter(pk = obj.pk, passing_masters__in=[ExecutantProfile.objects.get(user=self.user)]).exists()
            passings_executants = Assignment.objects.filter(passing_masters__in=[self.user.executantprofile])
            if not executants and obj.state == 'new':
                content += assignment_passing_button(obj, self.user.id)
        return content
    passing_action.allow_tags = True
    passing_action.short_description = 'Действия'
    passing_action.empty_value_display = 'Нет доступных действий'

    def response_change(self, request, obj):
        if obj.state == 'ready':
            project = Project.objects.get(assignment=obj.pk)
            return redirect(reverse('admin:crm_project_change', args=[project.pk]))
        else:
            return super(AssignmentAdmin, self).response_change(request, obj)

@admin.register(Project)
class ProjectAdmin(FSMTransitionMixin, BaseAdmin):
    #change_form_template = 'admin/fsm-transition/change_form.html'
    inlines = [
        InlineActivityAdmin,
        InlineInvoiceAdmin,
        InlinePriceAdmin,
    ]
    list_display = ['pk', 'state','address', 'assignment_phone_number', 'assignment_client_name']
    list_filter = ('state', )
    preserve_filters = True
    readonly_fields = ('state', 'assignment_phone_number', 'assignment_client_name')


    def get_fields(self, request, obj):
        if obj:
            if not request.user.is_superuser:
                if obj.state == 'complete_work':
                    return ['state', 'address', 'assignment_phone_number', 'assignment_client_name', 
                    'project_service', 'project_trouble']
                elif obj.state == 'started_diagnostic':
                    return ['state', 'address', 'assignment_phone_number', 'assignment_client_name', 
                    'diagnostic_service', 'diagnostic_trouble']
                elif obj.state == 'complete_project':
                    return ['state']
                else:
                    return ['state', 'address', 'assignment_phone_number', 'assignment_client_name']
        return super(ProjectAdmin, self).get_fields(request, obj)
    
    def get_inline_instances(self, request, obj):
        inlines = []
        if obj:
            if not request.user.is_superuser:
                print(obj.state)
                if obj.state == 'take_invoice':
                    for inline_class in self.inlines:
                        if inline_class is not InlineInvoiceAdmin:
                            inline = inline_class(self.model, self.admin_site)
                            inlines.append(inline)
                    return inlines
                elif obj.state == 'complete_project':
                    inlines = []
                    return inlines
                else:
                    for inline_class in self.inlines:
                        if inline_class is InlineActivityAdmin:
                            inline = inline_class(self.model, self.admin_site)
                            inlines.append(inline)
                        break
                    return inlines
        return super(ProjectAdmin, self).get_inline_instances(request, obj)

    
    def response_change(self, request, obj):
        if obj.state == 'get_invoice':
            invoice = Invoice.objects.filter(project=obj, state='wait_paid').last()
            return redirect(reverse('admin:crm_invoice_change', args=[invoice.pk]))
        else:
            return super(ProjectAdmin, self).response_change(request, obj)
    
    '''
    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            self.save_formset(request, form, formset, change=change)
        return super(ProjectAdmin, self).save_related(request, form, formsets, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        print("INSTANCES IS : " + str(instances))
        for instance in instances:
            print("INSTANCE IS : " + str(instance))
            instance.save()
        formset.save_m2m()
    '''
    def assignment_phone_number(self, obj):
        if obj.assignment:
            assignment_phone_number = PhoneNumber.objects.filter(leed=obj.assignment.appeal.leed).first()
            return assignment_phone_number
    assignment_phone_number.short_description = 'Номер телефона'
    assignment_phone_number.empty_value_display = 'Номер телефона не указан'

    def assignment_client_name(self, obj):
        if obj.assignment:
            if obj.assignment.client.user.first_name:
                return obj.assignment.client.user.first_name
            else:
                return None
    assignment_client_name.short_description = 'Имя клиента'
    assignment_client_name.empty_value_display = 'Имя не указано'


@admin.register(Leed)
class LeedAdmin(BaseAdmin):
    list_display_links = ['name']
    list_display = ['pk', 'name']

    def get_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['name', 'phone_number']
        return super(LeedAdmin, self).get_fields(request, obj)
    

@admin.register(Address)
class AddressAdmin(BaseAdmin):
    inlines = [InlineActivityAdmin]

    def get_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['geoposition', 'city', 'country', 'entrance', 'floor','flat']
        return super(AddressAdmin, self).get_fields(request, obj)


@admin.register(PriceList)
class PriceListAdmin(BaseAdmin):
    list_display = ['service', 'from_price', 'to_price', 'time']

    def get_list_display(self, request):
        self.user = request.user
        return super(PriceListAdmin, self).get_list_display(request)


@admin.register(Complaint)
class ComplaintAdmin(BaseAdmin):
    inlines = [InlineActivityAdmin]
    form = ComplaintForm

    def get_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['appeal', 'project']
        return super(ComplaintAdmin, self).get_fields(request, obj)


@admin.register(ClientProfile)
class ClietProfileAdmin(BaseAdmin):
    form = ClientForm

    def get_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['first_name', 'last_name', 'discount', 'legal_entity']
        return super(ClietProfileAdmin, self).get_fields(request, obj)

    def save_model(self, request, obj, form, change):
        user = User.objects.create(
            username=username_generator(),
            first_name=form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name'])
        obj.user = user
        return super(ClietProfileAdmin, self).save_model(request, obj, form, change)
 

@admin.register(ExecutantProfile)
class ExecutantProfileAdmin(BaseAdmin):
    inlines = [InlinePriceListAdmin]
    #readonly_fields = ['auth_action']
    def get_fields(self, request, obj):
        self.user = request.user
        if not request.user.is_superuser:
            return ['number_passport', 'serial_passport', 'work_cities', 'work_countries']#, 'auth_action']
        return super(ExecutantProfileAdmin, self).get_fields(request, obj)

    def get_readonly_fields(self, request, obj):
        if not request.user.is_superuser:
            return ('user', )
        return super(ExecutantProfileAdmin, self).get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super(ExecutantProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    '''
    def auth_action(self, obj):
        content = ""
        if self.executant and self.user.groups.filter(name='Masters').exists():
            content += telegram_auth_button(obj, self.user.id)
        return content
    auth_action.allow_tags = True
    auth_action.short_description = 'Авторизация'
    '''

@admin.register(Invoice)
class InvoiceAdmin(FSMTransitionMixin, BaseAdmin):
    readonly_fields = ['state', 'amount']
    list_display = ['pk', 'state', 'issue_date', 'project', 'amount']

    def get_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['state', 'amount']
        return super(InvoiceAdmin, self).get_fields(request, obj)

    def get_readonly_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['state', 'amount']
        return super(InvoiceAdmin, self).get_readonly_fields(request, obj)

    def response_change(self, request, obj):
        if obj.state == 'paid':
            return redirect(reverse('admin:crm_project_change', args=[obj.project.pk]))
        else:
            return super(InvoiceAdmin, self).response_change(request, obj)


@admin.register(Price)
class PriceAdmin(BaseAdmin):

    def get_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['project', 'service', 'trouble', 'time', 'price']
        return super(PriceAdmin, self).get_fields(request, obj)

    def get_readonly_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['project', 'service', 'trouble', 'time', 'price']
        return super(PriceAdmin, self).get_readonly_fields(request, obj)


@admin.register(Salary)
class SalaryAdmin(BaseAdmin):
    list_display = ['state', 'project', 'percent', 'amount', 'paid_amount']
    fields = ['state', 'project', 'percent', 'amount', 'paid_amount', 'content_object']
    readonly_fields = ['state', 'project', 'percent', 'amount', 'paid_amount']
    form = SalaryForm


@admin.register(PhoneNumber)
class PhoneNumberAdmin(BaseAdmin):
    def get_fields(self, request, obj):
        if not request.user.is_superuser:
            return ['phone_number']
        return super(PhoneNumberAdmin, self).get_fields(request, obj)


#@admin.register(Payment)
#class PaymentMethodAdmin(BaseAdmin):
#    form = PaymentForm
#    #fields = ['content_object']

admin.site.register(Bonus)
admin.site.register(Card)
#admin.site.register(PaymentType)
from django.contrib.auth.decorators import login_required
admin.site.logout = login_required(admin.site.logout)