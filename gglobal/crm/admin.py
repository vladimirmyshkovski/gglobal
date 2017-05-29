from django.contrib import admin
from allauth.account.utils import send_email_confirmation
from gglobal.users.models import User
from django.db import models
from django.utils.translation import ugettext as _
from gglobal.crm.forms import LeedForm, ActivityForm, ClientForm, ComplaintForm
from django.conf.urls import url
from django_object_actions import DjangoObjectActions
from django_admin_row_actions import AdminRowActionsMixin
from inline_actions.admin import InlineActionsMixin
from inline_actions.admin import InlineActionsModelAdminMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from gglobal.cms.models import MasterProfilePage, MastersIndexPage
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from functools import WRAPPER_ASSIGNMENTS, update_wrapper, wraps
from django.shortcuts import get_object_or_404
from webpush import send_user_notification
from jet.admin import CompactInline
from jet.filters import RelatedFieldAjaxListFilter
from admin_utils.mixins import FoldableListFilterAdminMixin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Avg
from django.contrib.admin.views.main import ChangeList
from .admin_buttons import appeal_river_field_button, appeal_river_button, \
                            assignment_river_field_button, assignment_river_button
from gglobal.crm.models import ClientProfile, MasterProfile, Invoice, \
                                Status, Activity, Project, PaymentMethod, \
                                PaymentType, Leed, Appeal, Source, \
                                Assignment, PhoneNumber, \
                                Complaint, Address, PriceList

from river.services.state import StateService
from django.contrib.contenttypes.models import ContentType
from .utils import username_generator
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline


admin.site.register(Invoice)
#admin.site.register(Status)
admin.site.register(Activity)
#admin.site.register(PaymentMethod)
#admin.site.register(PaymentType)
admin.site.register(PhoneNumber)
#admin.site.register(Source)
admin.site.register(MasterProfile)

#################
# INLINES ADMIN #


from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
class EditLinkToInlineObject(object):
    pass

class InlineAssigmentAdmin(CompactInline):
    model = Assignment
    max_num = 1
    #min_num = 0
    extra = 1

class InlineComplaintAdmin(CompactInline):
    model = Complaint
    max_num = 1
    #min_num = 0
    extra = 1

class InlineActivityAdmin(GenericStackedInline):
    model = Activity
    form = ActivityForm
    extra = 1

class InlineInvoiceAdmin(CompactInline):
    model = Invoice
    extra = 1


# END INLINES ADMIN #
#####################

@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ['service', 'trouble', 'from_price', 'to_price', 'time']

    def get_list_display(self, request):
        self.user = request.user
        return super(PriceListAdmin, self).get_list_display(request)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    inlines = [InlineActivityAdmin]
    form = ComplaintForm

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type', 'status', 'date', 'address', 'river_actions']
    list_filter = ('date', 'type', 'status')
    #readonly_fields = ['river_field_actions']
    #fields = ['river_field_actions']
    inlines = [InlineActivityAdmin]
    
    def get_queryset(self, request):
        qs = super(AssignmentAdmin, self).get_queryset(request)
        if request.user.is_superuser or not request.user.groups.filter(name='Masters').exists():
            return qs
        master = MasterProfile.objects.get(user=request.user)
        return qs.filter(address__city__in=master.work_cities, master__isnull=True).all()

    def get_readonly_fields(self, request, obj):
        if obj:
            if request.user.groups.filter(name='Masters').exists():
                return ['type', 'client', 'trouble', 'service', 'appeal', 'date', 'address', 'river_field_actions']
        return super(AssignmentAdmin, self).get_readonly_fields(request, obj)

    def get_list_display(self, request):
        self.user = request.user
        return super(AssignmentAdmin, self).get_list_display(request)

    def get_fields(self, request, obj):
        if obj:
            #if obj.get_available_proceedings(request.user):
            #    print('fatherfucker')
            if request.user.groups.filter(name='Masters').exists():
                return ['type', 'client', 'trouble', 'service', 'appeal', 'date', 'address', 'river_field_actions']
        return super(AssignmentAdmin, self).get_fields(request, obj)

    def save_model(self, request, obj, form, change):
        pass



    # BUTTONS #
    def river_field_actions(self, obj):
        content = ""
        for proceeding in obj.get_available_proceedings(self.user):
            content += assignment_river_field_button(obj, proceeding)
        return content
    river_field_actions.allow_tags = True
    river_field_actions.short_description = 'Действия'
    river_field_actions.empty_value_display = 'Нет доступных действий'

    def river_actions(self, obj):
        content = ""
        for proceeding in obj.get_available_proceedings(self.user):
            content += assignment_river_button(obj, proceeding)
        return content
    river_actions.allow_tags = True
    river_actions.short_description = 'Действия'
    river_actions.empty_value_display = 'Нет доступных действий'
    # END BUTTONS #





@admin.register(ClientProfile)
class ClietAdmin(admin.ModelAdmin):
    form = ClientForm

    def save_model(self, request, obj, form, change):
        if not obj.username:
            try:
                obj.username = username_generator()
            except:
                pass
        return super(ClietAdmin, self).save_model(request, obj, form, change)



@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    #inline_type = 'stacked'
    #inline_reverse = [('assigment', {'fields': ['trouble', 'service', 'client', 'type', 'address']}),
    # 'complaint']

    search_fields = ['id', '@leed__phone_number__phone_number']

    inlines = [
        InlineAssigmentAdmin,
        InlineComplaintAdmin,
        InlineActivityAdmin
    ]

    def phone_numbser(self, obj):
        if not obj.status.id == 1: 
            phone_number = PhoneNumber.objects.filter(leed=obj.leed).first()
            return phone_number


    phone_numbser.short_description = 'Номера телефона лида'
    phone_numbser.empty_value_display = 'Сначала нажми на "Принять"'

    #inlines = [
    #    InlineAssigmentAdmin
    #]
    #list_display_links = ['pk']
    list_display = ['pk', 'status', 'type', 'phone_numbser', 'river_actions']
    #fields = ('type','river_field_actions')
    '''
    fieldsets = (
        (None, {
            'fields': ('type', 'river_field_actions')
        }),
        ('Обратившийся', {
            'classes': ('collapse',),
            'fields': ('leed', ),
        }),
    )
    '''
    readonly_fields = ('river_field_actions',)
    #search_fields = ['leed__name']
    list_select_related = True
    list_filter = ('status', 'type', 'source')
    #form = ConsumerRegistrationForm


    def get_list_display(self, request):
        self.user = request.user
        return super(AppealAdmin, self).get_list_display(request)

    def get_fields(self, request, obj):
        self.user = request.user
        if obj:
            if not request.user.is_superuser:
                if obj.status == StateService.get_initial_state(ContentType.objects.get_for_model(Appeal)):
                    return ('source', 'type', 'activities', 'river_field_actions')
                if not obj.get_available_proceedings(request.user):
                    return ('activities', )
                else:
                    ('source', 'type', 'leed', 'activities', 'river_field_actions')
        return super(AppealAdmin, self).get_fields(request, obj)

    def get_inline_instances(self, request, obj):
        if not request.user.is_superuser:
            if not obj.get_available_proceedings(request.user):
                return []
        return super(AppealAdmin, self).get_inline_instances(request, obj)    

    # BUTTONS #
    def river_field_actions(self, obj):
        content = ""
        for proceeding in obj.get_available_proceedings(self.user):
            content += appeal_river_field_button(obj, proceeding)

        return content
    
    river_field_actions.allow_tags = True
    river_field_actions.short_description = 'Действия'
    river_field_actions.empty_value_display = 'Нет доступных действий'
    def river_actions(self, obj):
        content = ""
        for proceeding in obj.get_available_proceedings(self.user):
            content += appeal_river_button(obj, proceeding)

        return content
    river_actions.allow_tags = True
    river_actions.short_description = 'Действия'
    river_actions.empty_value_display = 'Нет доступных действий'
    # END BUTTONS #

    
    def save_model(self, request, obj, form, change):
        if 'type' in form.changed_data and obj.type == 'order':

            return self.fields 
        super(AppealAdmin, self).save_model(request, obj, form, change)
    

    #def save_model(self, request, obj, form, change):
    #    if not obj.pk: # call super method if object has no primary key 
    #        super(AppealAdmin, self).save_model(request, obj, form, change)
    #    else:
    #        pass # don't actually save the parent instance


    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            print('formset : ' + str(formset.model) + 'change :' + str(change))
            self.save_formset(request, form, formset, change=change)
        super(AppealAdmin, self).save_model(request, form.instance, form, change)

    '''
    def has_add_permission(self, request):
        return request.user.groups.filter(name='Managers').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='Managers').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    '''
    @staticmethod
    def autocomplete_search_fields():
        return 'leed'

@admin.register(Leed)
class LeedAdmin(admin.ModelAdmin):
    list_display_links = ['name']
    list_display = ['name', 'text', 'city']
    fields = ['name']
    form = LeedForm
    add_form = LeedForm

    '''
    def get_fields(self, request, obj):
        if obj:
            if not request.user.is_superuser:
                try:
                    appeal = get_object_or_404(Appeal, leed=obj)
                    if appeal.status_id == 1:
                        return ['name', 'text', 'trouble', 'service']
                except:
                    pass
            else:
                return ['name','text', 'phone_number', 'trouble', 'service', 'city', 'site', 'form']

        return super(LeedAdmin, self).get_fields(request, obj)
    '''

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    inlines = [InlineActivityAdmin]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        InlineActivityAdmin,
        InlineInvoiceAdmin
    ]

    