from django import forms
from .models import Sets, Repeats

class SetForm(forms.ModelForm):
	class Meta:
		model = Sets
		fields = ['date', 'user', 'exercise']


class RepeatsForm(forms.ModelForm):
	class Meta:
		model = Repeats
		fields = ['set', 'weight', 'repeats']