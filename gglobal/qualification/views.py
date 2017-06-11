from django.shortcuts import render, get_object_or_404, reverse, redirect
from gglobal.qa.models import Question, Answer
from django.template import loader
from django.http import Http404
from gglobal.qualification.forms import QualificationAnswerForm
from django.views import generic
from gglobal.qa.mixins import LoginRequired
from django.conf import settings
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper

try:
    qa_messages = 'django.contrib.messages' in settings.INSTALLED_APPS and\
        settings.QA_MESSAGES
except AttributeError:
    qa_messages = False

if qa_messages:
    from django.contrib import messages


class IndexView(generic.ListView):
    template_name = 'qualification/qualification.html'
    context_object_name = 'index'


    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(answer__isnull=True).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    context_object_name = 'detail'
    template_name = 'qualification/question.html'

    def get_context_data(self, **kwargs):
        #self.helper = FormHelper(self)
        #self.helper.form_action = reverse('create_answer', kwargs={'question_id': self.kwargs['question_id']})
        context = super(DetailView, self).get_context_data(**kwargs)
        form = QualificationAnswerForm()
        form.helper.form_action = reverse('qualification:answer', kwargs={'question_id': self.kwargs.get("question_id")})
        context['form'] = form
        return context

    def get_object(self):
        return get_object_or_404(Question, pk=self.kwargs.get("question_id"))


class CreateAnswerView(generic.CreateView):
    """
    View to create new answers for a given question
    """
    context_object_name = 'answer'
    form_class = QualificationAnswerForm
    template_name = 'qualification/question.html'
    message = _('Thank you! your answer has been posted.')

    #def get_form(self, form_class=None):
    #    form = super(CreateAnswerView, self).get_form(form_class)
    #    form.helper.form_action = ""
    #    return form      

    def form_valid(self, form):
        """
        Creates the required relationship between answer
        and user/question
        """
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(CreateAnswerView, self).form_valid(form)


    def get_success_url(self):
        if qa_messages:
            messages.success(
                self.request, self.message)
        return reverse('qualification:detail', kwargs={'question_id': self.kwargs['question_id']})


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

