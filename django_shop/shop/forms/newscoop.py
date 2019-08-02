from __future__ import unicode_literals

from django.conf import settings
from django.db.models import Max
from django.forms import models, fields, widgets,forms
from django.utils.translation import ugettext_lazy as _
from cms.wizards.forms import BaseFormMixin
from djangocms_text_ckeditor.fields import HTMLFormField
from djng.forms import NgModelForm
from shop.models.related import ProductPageModel
from djng.styling.bootstrap3.forms import Bootstrap3ModelForm
from django import forms
from cms.forms.fields import PageSelectFormField
from myshop.models.polymorphic_.scoop import Scoop
from myshop.models.polymorphic_ import Product
from cmsplugin_cascade.link.forms import LinkForm
from cms.models.pagemodel import Page
from myshop.models.manufacturer import Manufacturer
from shop.admin.product import CMSPageAsCategoryMixin, ProductImageInline, InvalidateProductCacheMixin, CMSPageFilter


class ScoopWizardForm(forms.ModelForm,LinkForm):

    form_name="create_scoop"
    scope_prefix = 'innerscope'
    legend = _("scoop details")

    product_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write a name...'
        }
    ))

    product_code = forms.IntegerField(widget= forms.NumberInput(

        attrs={
            'class': 'form-control',
            'placeholder': 'enter code...'
        }


    ))

    time_duration = forms.TimeField(widget=forms.TimeInput(

        attrs={
            'class': 'form-control',
            'placeholder': 'enter time...'


        }

    ))
    caption = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write a caption...'
        }
    ))

    description = forms.CharField(widget=forms.TextInput(

        attrs={

            'class': 'form-control',
            'placeholder': 'Write a description...'

        }
    ))

    manufacturer = forms.ModelChoiceField(
        required=False,
        queryset=Manufacturer.objects.all(),
        label='',
        help_text=_("Top seller or Top rated"),

    )





    class Meta:
        model = Product
        fields = ('product_name', 'slug', 'caption', 'description', 'product_code', 'manufacturer',
              'unit_price', 'active', 'images',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(ScoopWizardForm, self).__init__(*args, **kwargs)
        self.fields['user_defined_code'] = forms.ModelChoiceField(queryset=Product.objects.filter(manufacturer=Manufacturer))

