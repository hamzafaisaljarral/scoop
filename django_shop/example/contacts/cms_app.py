# -*- coding: utf-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class ContactFormApphook(CMSApp):
    name = u"Contact"
    def get_urls(self, page=None, language=None, **kwargs):
        return ["myshop.urls.examples"]



apphook_pool.register(ContactFormApphook)
