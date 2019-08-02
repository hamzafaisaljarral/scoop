from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from email_auth.models import User

from jobs.models import Jobs,ProfileJob
from . import widgets
from django.forms import DateInput


class SearchForm(forms.Form):
    title = forms.CharField()
    location = forms.EmailField()


