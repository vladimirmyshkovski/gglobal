from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from gglobal.qa.models import (UserQAProfile, Question, Answer, MyCustomTag, AnswerVote, AnswerComment, QuestionComment)


admin.site.register(UserQAProfile)
admin.site.register(Question)
admin.site.register(Answer, MarkdownxModelAdmin)
admin.site.register(AnswerComment)
admin.site.register(QuestionComment)
admin.site.register(MyCustomTag)
admin.site.register(AnswerVote)