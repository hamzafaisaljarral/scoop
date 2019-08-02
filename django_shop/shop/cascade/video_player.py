from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.forms.fields import CharField
from django.forms import widgets
from django.template import engines
from django.template.loader import select_template
from django.utils.html import strip_tags, format_html
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _, pgettext_lazy
try:
    from html.parser import HTMLParser  # py3
except ImportError:
    from HTMLParser import HTMLParser  # py2
from cms.plugin_pool import plugin_pool

from djangocms_text_ckeditor.widgets import TextEditorWidget
from djangocms_text_ckeditor.utils import plugin_tags_to_user_html
from djangocms_text_ckeditor.cms_plugins import TextPlugin

from cmsplugin_cascade.fields import GlossaryField
from cmsplugin_cascade.strides import strides_plugin_map, strides_element_map, TextStridePlugin, TextStrideElement
from cmsplugin_cascade.link.cms_plugins import TextLinkPlugin
from cmsplugin_cascade.link.forms import LinkForm, TextLinkFormMixin
from cmsplugin_cascade.link.plugin_base import LinkElementMixin
from cmsplugin_cascade.plugin_base import TransparentContainer
from cmsplugin_cascade.bootstrap3.buttons import BootstrapButtonMixin

from shop.conf import app_settings
from shop.forms.checkout import AcceptConditionForm
from shop.models.cart import CartModel
from myshop.models.polymorphic_.scoop import Scoop
from django.template.defaultfilters import slugify

from shop.admin.product import CMSPageAsCategoryMixin, ProductImageInline, InvalidateProductCacheMixin, CMSPageFilter
from shop.modifiers.pool import cart_modifiers_pool
from .plugin_base import ShopPluginBase, ShopButtonPluginBase, DialogFormPluginBase
from cmsplugin_cascade.plugin_base import CascadePluginBase


class VideoPlayer(ShopPluginBase):
    form_class = 'shop.forms.newscoop.ScoopWizardForm'
    name = "My Video player"

    render_template = 'shop/scoopform/Videoplayer.html'

    pass


plugin_pool.register_plugin(VideoPlayer)



