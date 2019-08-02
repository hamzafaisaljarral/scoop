# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.core.urlresolvers import  reverse
from django.utils import timezone
from shop.models.defaults.mapping import ProductPage, ProductImage
from PIL import Image
from email_auth.models import User
from jobs.models import Jobbid,Jobs,ProfileJob
from profile import models as production


from django.db.models.signals import post_save
from django.dispatch import receiver

from cms.models import CMSPlugin







class Hire(models.Model):

    #
    # NOTE: Everything in this section should be optional, fields are to be
    # made Required in the Forms.
    #

    hiredprofile = models.ForeignKey(production.Profile,on_delete=models.CASCADE,null=True, blank=True)
    jobhiredfor = models.ForeignKey(Jobs,on_delete=models.CASCADE,null=True, blank=True)
    profileofjobpublisher = models.ForeignKey(ProfileJob,on_delete=models.CASCADE,null=True, blank=True)

    message = models.TextField(u'message project detail to freelancer',
        blank=True,
        default='',
        help_text=u'Enter project details or anything else you want freelancer to know.',

    )

    price = models.DecimalField(max_digits=100, decimal_places=2)
    is_accepted = models.BooleanField(default=True)
    is_rejected = models.BooleanField(default=False)
    end_date = models.DateTimeField(u'when will your event end', blank=True,
                                    default=timezone.now,
                                    help_text=u'enter the date when your project will end.', )





    def __str__(self):
        return self.message




    # Meta, non-form data
    contact_date = models.DateTimeField(u'contact date',
                                        blank=True,
                                        default=timezone.now,
                                        help_text=u'When this person completed the contact form.',
                                        )

    was_contacted = models.BooleanField(u'has been contacted?',
                                        default=False,
                                        help_text=u'Check this if someone has already reached out to this person.',
                                        )

    notes = models.TextField(u'contact notes',
                             blank=True,
                             default='',
                             help_text=u'Internal notes relating to contacting this person.',
                             )

    referer = models.CharField(u'referring page',
                               blank=True,
                               default='',
                               help_text=u'This is the page the visitor was on before coming to the contact page.',
                               max_length=2048,
                               )

    def send_notification_email(self):
        """
        Sends a notification email to the list of recipients defined in
        settings.NOTIFICATIONS informing them that a new contact has arrived.

        SERVER_EMAIL is defined in settings and contacts the "from"
        address for email sent from the webserver.

        MANAGERS needs to be defined in settings and should be a list
        containing the email addresses of those that should receive
        notification of an incoming contact.
        """

        # Using a template is probably overkill for this but...
        email_subject = render_to_string('contacts/notification-subject.txt', {
            'contact': self,
        })

        email_body = render_to_string('contacts/notification-body.txt', {
            'contact': self,
        })

        try:
            send_mail(
                email_subject,
                email_body,
                settings.SERVER_EMAIL,
                settings.MANAGERS,
                fail_silently=(not settings.DEBUG)
            )

        except Exception:
            # If NOT in DEBUG (development) mode, we silently ignore any
            # exceptions to avoid interrupting capture of the submitter's
            # details. If in DEBUG mode, then raise the error so we can
            # troubleshoot.
            if (settings.DEBUG):
                raise

    def save(self, *args, **kwargs):

        if not self.pk:
            #
            # If using something like Celery, then this should be scheduled, not
            # executed in the request/response cycle.
            #
            try:
                self.send_notification_email()
            except:
                #
                # This is just a precaution, should there be an issue with the
                # emailing, we do not want this to prevent the new Contact
                # object from being saved.
                #
                pass

        super(Hire, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s (%s)' % (self.message, str(self.contact_date),)





class HirePluginModel(CMSPlugin):

    title = models.CharField(u'title',
        blank=True,
        help_text=u'Optional. Title of the widget.',
        max_length=64,
    )


    def __unicode__(self):
        return self.title


class Subscription(models.Model):
	hires = models.ForeignKey(Hire,related_name='subscription')
	payment_nonce = models.CharField(max_length=100,null=True,blank=True)
	amount = models.CharField(max_length=100,null=True,blank=True)
	txnid = models.CharField(max_length=25,null=True,blank=True)
	result = models.BooleanField(default=False)


	def __str__(self):
		return self.hires.profileofjobpublisher.name
