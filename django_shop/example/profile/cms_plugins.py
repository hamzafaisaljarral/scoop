# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse_lazy,reverse

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import ProfilePluginModel
from .forms import ProfileAjaxForm



class ProfilePlugin(CMSPluginBase):
    model = ProfilePluginModel
    name = _("Blog Form")
    render_template = "contacts/_contact_widget.html"


    def render(self, context, instance, placeholder):

        #
        # NOTE: We're actually interested in the request.path here, NOT the
        # referer, since this form will appear alongside real content, unlike
        # the contact form page, which is standalone.
        #
        try:
            path = context['request'].path
        except:
            path = ''

        form = ProfileAjaxForm(initial={'referer': path})

        context.update({
            "title": instance.title,
            "form": form,
            "form_action": reverse("blogging_form"),
        })
        return context

plugin_pool.register_plugin(ProfilePlugin)


