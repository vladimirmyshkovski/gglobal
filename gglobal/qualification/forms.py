from django import forms
from django.utils.translation import ugettext_lazy as _
from gglobal.qa.models import Answer
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Submit
from django.core.urlresolvers import reverse


class QualificationAnswerForm(forms.ModelForm):
	answer_text = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = Answer
		fields = ['answer_text']

	def __init__(self, *args, **kwargs):
		super(QualificationAnswerForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_method = "POST"
		# Add submit button like in original form.
		#self.helper.add_input(Submit('submit', _('Submit'), css_class='btn btn-custom btn-sm btn-block'))
		self.helper.layout.append(
			HTML("<button style='width: 15rem' class='col-xs-offset-4 col-md-offset-5 btn btn-custom btn-sm btn-block' type='submit'>"
				"%s</button>" % _('Answer')
				)
			)
		self.helper.form_action = ''
		self.helper.form_class = ''
		self.helper.label_class = 'hidden'
		self.helper.field_class = ''

