from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from gglobal.qa.models import Question, Answer
from django.utils.translation import ugettext_lazy as _


class AnswerModelAdmin(ModelAdmin):
	model = Answer
	menu_label = (_('Ответы'))


class QuestionModelAdmin(ModelAdmin):
	model = Question
	menu_label = (_('Вопросы'))

class QAModelAdminGroup(ModelAdminGroup):
	menu_label = (_('Вопросы/Ответы'))
	menu_icon = 'fa-question'
	menu_order = 500
	items = (QuestionModelAdmin, AnswerModelAdmin)

modeladmin_register(QAModelAdminGroup)	