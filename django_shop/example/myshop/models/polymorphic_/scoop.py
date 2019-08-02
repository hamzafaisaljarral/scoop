from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField

from shop.money.fields import MoneyField

from .product import Product, BaseProductManager
from embed_video.fields import EmbedVideoField


class Scoop(Product):
    # common product fields
    unit_price = MoneyField(
        _("Unit price"),
        decimal_places=3,
        help_text=_("Net price for this product"),
    )

    # product properties


    product_code = models.CharField(
        _("Product code"),
        max_length=255,
        unique=True,
    )



    time_duration = models.PositiveIntegerField(
        _("time duration"),
        help_text=_("time in days"),
    )

    description = HTMLField(
        verbose_name=_("Description"),
        configuration='CKEDITOR_SETTINGS_DESCRIPTION',
        help_text=_("Full description used in the catalog's detail view of Scoop."),
    )


    default_manager = BaseProductManager()

    class Meta:
        verbose_name = _("Scoop")
        verbose_name_plural = _("Scoop")

    def get_price(self, request):
        return self.unit_price
