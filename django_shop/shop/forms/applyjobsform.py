from django import forms

from jobs.models import Jobbid


class Applyjobsform(forms.ModelForm):
    class Meta:
       model = Jobbid

       fields = {'price','Details'}
       required_fields = ['price', 'Details']
