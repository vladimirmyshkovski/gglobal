from django.contrib import admin

from gglobal.badges.models import Badge
from gglobal.users.models import User


class InlineBadgeToUser(admin.StackedInline):
	model = User.badges.through

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    fields = ('icon', 'level')
    list_display = ('id','level')
    inlines = [InlineBadgeToUser]


