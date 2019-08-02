# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers


from shop.forms.newscoop import (
    ScoopWizardForm)


class ScoopSerializer(serializers.ModelSerializer):
    scoop_tag = serializers.SerializerMethodField()


    def get_scoop_tag(self, Scoop):
        try:
            form = ScoopWizardForm(instance=Scoop.objects.all())
            return form.as_text()
        except AttributeError:
            return



