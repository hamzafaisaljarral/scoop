# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm

from .models import Jobs


class JobBaseForm(ModelForm):
    class Meta:
        abstract = True

    required_css_class = 'required'

    #
    # To help prevent people sending a typo’ed email address, then wondering
    # why we never got back to them, we'll require them to provide their email
    # twice.
    #
    verify_email = forms.EmailField(
        label=u'Verify email',
        help_text=u'Please retype your email address here.',
        max_length=255,
        required=True,
    )

    required_fields = []



class JobForm(JobBaseForm):

    images=forms.ImageField(help_text="Upload image: ", required=False)

    class Meta:
        model = Jobs
        fields = [
            'type','images', 'description',
        ]



    required_fields = ['type', 'email', 'verify_email', ]



class JobAjaxForm(JobBaseForm):
    images=forms.ImageField(help_text="Upload image: ", required=False)
    class Meta:
        model = Jobs
        fields = ['type','images', 'description', ]






