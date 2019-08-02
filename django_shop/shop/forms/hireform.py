from django import forms
from django.contrib.admin import widgets
from django.forms import DateInput

from . import widgets

from hire.models import Hire


class Hireform(forms.ModelForm):
    class Meta:
       model = Hire



       fields = {'message'}

       required_fields = ['message']



