from gglobal.qa.models import UserQAProfile, Question
from django.conf import settings
from django import forms
from gglobal.qa.models import MyCustomTag

from dal import autocomplete

class QuestionForm(autocomplete.FutureModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=MyCustomTag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url='qa_tag_autocomplete',
            attrs={'data-html': 'true'}
            )
        )
    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        if hasattr(settings, 'QA_DESCRIPTION_OPTIONAL'):
            self.fields['description'].required = not settings.QA_DESCRIPTION_OPTIONAL
