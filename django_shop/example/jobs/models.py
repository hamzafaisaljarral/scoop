# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.core.urlresolvers import  reverse
from django.utils import timezone
from email_auth.models import User

from profile import models as production

from shop.models.defaults.mapping import ProductPage, ProductImage
from PIL import Image


from cms.models import CMSPlugin





class ProfileJob(models.Model):

    #
    # NOTE: Everything in this section should be optional, fields are to be
    # made Required in the Forms.
    #


    name = models.CharField(u'Name',
        blank=False,
        default='',
        help_text=u'Your name',
        max_length=64,
    )

    aboutyou = models.TextField(u'About you',
         blank=False,
         default='',
         help_text=u'About you.',
    )


    profileimage = models.ImageField(
        upload_to='profile_image',
        blank=False
    )



    location = models.CharField(u'your location',
        blank=False,
        default='',
        help_text=u'your location.',
        max_length=64,
    )


    address = models.CharField(u'Enter your phone number',
                                   blank=False,
                                   default='',
                                   help_text=u'enter your phone number ',
                                   max_length=64,

                                   )

    account = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default='')

    customer_id = models.CharField(max_length=25, null=True, blank=True)
    client_token = models.TextField(verbose_name=u'client token', max_length=500,null='True')
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

    def __unicode__(self):
        return self.name


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

        super(ProfileJob, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s (%s)' % (self.name, str(self.contact_date),)


class Jobs(models.Model):

    #
    # NOTE: Everything in this section should be optional, fields are to be
    # made Required in the Forms.
    #


    type = models.CharField(u'Name',
        blank=False,
        default='',
        help_text=u'Your name',
        max_length=64,
    )

    title = models.TextField(u'skills',
         blank=False,
         default='',
         help_text=u'what kind of skills you are looking for.',
    )


    images = models.ImageField(
        upload_to='profile_image',
        blank=False,

    )

    start_date = models.DateTimeField(u'enter the date when you want it  ',
                                        blank=False,
                                        default=timezone.now,
                                        help_text=u'enter the date of project.',
                                        )
    description =  models.TextField(u'Enter the description',
        blank=False,
        default='',
        help_text=u'enter the description of job.',
    )

    location = models.CharField(u'your location',
        blank=False,
        default='',
        help_text=u'your location.',
        max_length=64,
    )
    end_date = models.DateTimeField(u'when will your event end', blank=False,
                                        default=timezone.now,
                                        help_text=u'enter the date when your project will end.', )
    price = models.IntegerField(u'enter the price you willing to pay ',
         blank=False,
         default='',
         help_text=u'enter your hourly price willing to pay in $'

    )

    jobprofile = models.ForeignKey(ProfileJob,on_delete=models.CASCADE,null=True, blank=True)








class Jobbid(models.Model):

    Yourprofile = models.ForeignKey(production.Profile,on_delete=models.CASCADE,null=True, blank=True)
    jobappliedto = models.ForeignKey(Jobs,on_delete=models.CASCADE,null=True, blank=True)

    pub_date = models.DateTimeField(u'date published',
        blank=True,
        default=timezone.now,
                                    )
    price = models.IntegerField(
         blank=True,
         default='',
         help_text=u'enter your offer price $')
    Details = models.CharField(max_length=200)






class JobPluginModel(CMSPlugin):

    title = models.CharField(u'title',
        blank=True,
        help_text=u'Optional. Title of the widget.',
        max_length=64,
    )


    def __unicode__(self):
        return self.title


