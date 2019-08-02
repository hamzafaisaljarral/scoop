
from __future__ import unicode_literals

import self
from django.forms.widgets import Select
from django.utils.translation import ugettext_lazy as _
from django_filters import FilterSet
from jobs.models import Jobbid,Jobs
from django.db import models
import django_filters

class dateFilter(django_filters.FilterSet):
    date = django_filters.NumberFilter(name='date_joined', lookup_expr='year')
    class Meta:
        model = Jobbid

        fields = ['date',]



