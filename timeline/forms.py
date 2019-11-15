
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms import ModelForm
# from django.forms.extras import SelectDateWidget

from .models import Hyuga_Requests


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder':'Username'}))
    password = forms.CharField(label="", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder':'Password'}))

# from functools import partial
# DateInput = partial(forms.DateInput, {'class': 'datepicker', 'placeholder':'click for calendar','label':'Date'},)


class HyugaRequestForm(forms.Form):
    halfday_setting = forms.CharField(label="halfday_setting", max_length=1)
    start_date = forms.DateField(label="start_date")
    end_date = forms.DateField(label="end_date", required=False)
    reason = forms.CharField(label="reason", max_length=100)