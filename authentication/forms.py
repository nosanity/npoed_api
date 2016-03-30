# coding: utf8

from django import forms
from authentication.models import RegisteredApp


class RegisterAppForm(forms.ModelForm):
    class Meta:
        model = RegisteredApp
        fields = ['url']
