from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from gglobal.qa.models import (UserQAProfile, Question, Answer, MyCustomTag, AnswerVote, AnswerComment, QuestionComment)


admin.site.register(UserQAProfile)
admin.site.register(Question)
admin.site.register(Answer, MarkdownModelAdmin)
admin.site.register(AnswerComment)
admin.site.register(QuestionComment)
admin.site.register(MyCustomTag)
admin.site.register(AnswerVote)