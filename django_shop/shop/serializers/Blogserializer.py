from __future__ import unicode_literals

from django.core import exceptions
from django.core.cache import cache
from django.template import TemplateDoesNotExist
from django.template.loader import select_template
from django.utils.html import strip_spaces_between_tags
from django.utils import six
from django.utils.safestring import mark_safe, SafeText
from django.utils.translation import get_language_from_request

from rest_framework import serializers

from shop.conf import app_settings
from Blogging.models import Blogs
from shop.models.customer import CustomerModel
from shop.models.product import ProductModel
from shop.models.order import OrderItemModel
from shop.rest.money import MoneyField

class BloggingSerializer(serializers.ModelSerializer):
    """
    Common serializer for our Contact model.
    """


    class Meta:
        model = Blogs
        fields = '__all__'

