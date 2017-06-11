from guardian.models import UserObjectPermission
from django.contrib.auth.models import Group
from guardian.models import UserObjectPermission
from gglobal.cms.models import ExecutantIndexPage, ExecutantProfilePage
from allauth.account.utils import send_email_confirmation
from gglobal.crm.models import ExecutantProfile

def add_to_master_group(modeladmin, request, queryset):
	group = Group.objects.get(name="Masters")
	for master in queryset:
		group.user_set.add(master)
		executantprofile = ExecutantProfile.objects.get(user=master)
		group.save()
		UserObjectPermission.objects.assign_perm('change_executantprofile', master, obj=executantprofile)
add_to_master_group.short_description = 'Добавить мастеров в группу'

def add_to_manager_group(modeladmin, request, queryset):
	group = Group.objects.get(name="Managers")
	for master in queryset:
		group.user_set.add(master)
		group.save()
		#UserObjectPermission.objects.assign_perm('change_executantprofile', master, obj=group)
add_to_manager_group.short_description = 'Добавить менеджеров в группу'

def create_master_page(modeladmin, request, queryset):
	parent_page = ExecutantIndexPage.objects.first()
	for master in queryset:
		page = ExecutantProfilePage.objects.create(
			title=master.slug,
			owner=master,
			)
		parent_page.add_child(page)
		parent_page.save()
create_master_page.short_description = 'Создать страницу для мастера'

def send_email_confirm(modeladmin, request, queryset):
    for master in queryset:
        user = User.objects.get(pk=master.user.pk)
        send_email_confirmation(request, user, signup=False)
send_email_confirm.short_description = 'Отправить письмо с подтверждением электронной почты'

