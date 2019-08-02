# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ungettext

from .models import Profile



class Profileadmin(admin.ModelAdmin):
    list_display = ('name','city','profileimage','samplework1','samplework2','samplework3','samplework4','price','DOB','webpage','organization','skills','location','phonenumber','account', )

    fieldsets = (
        (None, {
            'fields': (
                'name','city', 'profileimage','samplework1','samplework2','samplework3','samplework4','price', 'DOB', 'webpage', 'organization', 'skills', 'location',
                'phonenumber','account',



            ),
        }),
        (_(u'Description'), {
            'fields': (
                'description',
            )
        }),
        (_(u'city'), {
            'fields': (
                'city',
            )
        }),

        (_(u'Internal'), {
            'classes': ('collapse',),
            'fields': (
                'contact_date',
                'was_contacted',
                'notes',
            ),
        }),
        (_(u'Refering page'), {
            'fields': (
                'referer',
            ),
        }),
    )

    def set_was_contacted(self, request, queryset):
        affected = queryset.update(was_contacted=True)
        kind = self.model._meta.verbose_name.title() if affected == 1 else self.model._meta.verbose_name_plural.title()
        self.message_user(request,
                          ungettext(u"%(num)d %(kind)s was set as contacted", "%(num)d %(kind)s were set as contacted",
                                    affected) % {'num': affected, 'kind': kind})

    def unset_was_contacted(self, request, queryset):
        affected = queryset.update(was_contacted=False)
        kind = self.model._meta.verbose_name.title() if affected == 1 else self.model._meta.verbose_name_plural.title()
        self.message_user(request, ungettext(u"%(num)d %(kind)s was unset as contacted",
                                             "%(num)d %(kind)s were unset as contacted", affected) % {'num': affected,
                                                                                                      'kind': kind})


admin.site.register(Profile,Profileadmin,)
