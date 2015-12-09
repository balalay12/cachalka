from django import forms
from .models import Sets, Repeats, BodySize


class SetForm(forms.ModelForm):
    class Meta:
        model = Sets
        fields = ['date', 'user', 'exercise']


class RepeatsForm(forms.ModelForm):
    class Meta:
        model = Repeats
        fields = ['set', 'weight', 'repeats']


class BodySizeForm(forms.ModelForm):
    class Meta:
        model = BodySize
        fields = ['date', 'chest', 'waist', 'hip', 'arm', 'weight', 'user']
