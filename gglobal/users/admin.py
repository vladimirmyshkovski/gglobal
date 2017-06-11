# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User
from gglobal.crm.admin import InlineExecutantProfileAdmin, InlineClientProfileAdmin, InlinePhoneNumberAdmin
from gglobal.crm.actions import add_to_manager_group, add_to_master_group, create_master_page, send_email_confirm

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

@admin.register(User)
class MyUserAdmin(AuthUserAdmin):

    form = MyUserChangeForm
    add_form = MyUserCreationForm
    #inlines = [InlinePhoneNumberAdmin]
    fieldsets = (
            ('Профиль пользователя', {'fields': (
                'sites', 'raiting', 
                'first_name', 'last_name'
                )}
            ),
    ) + AuthUserAdmin.fieldsets
    list_display = ('username', 'is_superuser')
    search_fields = ['username', 'first_name', 'last_name']
    actions = [add_to_master_group, add_to_manager_group,create_master_page, send_email_confirm]
    def get_actions(self, request):
        actions = super(MyUserAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            if 'add_to_master_group' and 'add_to_manager_group' and 'create_master_page' and 'send_email_confirm' in actions:
                del actions['delete_selected']
                del actions['create_master_page']
                del actions['send_email_confirm']
                del actions['add_to_master_group']
                del actions['add_to_manager_group']
        return actions

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(MyUserAdmin, self).get_inline_instances(request, obj)

    def get_fields(self, request, obj):
        if obj:
            if not request.user.is_superuser:
                return ['phone_number', 'address']
        return super(MyUserAdmin, self).get_fields(request, obj)

    def get_inline_instances(self, request, obj):
        if obj:
            if not request.user.is_superuser:
                return [MasterInlineAdmin]
        return super(MyUserAdmin, self).get_inline_instances(request, obj)

    class Media:
        js = ("/static/js/admin/instantsearch.js",)