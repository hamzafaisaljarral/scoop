# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from shop.views.auth import PasswordResetConfirm
from cms.sitemaps import CMSSitemap
from myshop.sitemap import ProductSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import  url
from django.core.urlresolvers import reverse
from django.conf.urls import url
from rest_framework import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter


from profile.views import ProfileFormView,ProfileFormAjaxView
from contacts.views import ContactFormView, ContactFormAjaxView,ContactDisplay
from shop.views.jobprofile import upload
from shop.views.profileview import uploadprofile,freelancerSignUpView
from shop.views.jobprofile import Applyjob,addjobbid
from Blogging.views import BlogFormAjaxView,BlogFormView
from shop.views.blogview import BlogList,BlogRetrieveView
from shop.views.jobprofile import jobindex,jobupdateDetails,JobpublisherSignUpView,displayjob,JobListing,searching
from shop.views.jobprofile import profileupload,mapsearch
from shop.views.hireview import jobbidoffer,Tasklisting,offers,Accepted,Rejected,cashwithdraw,success,Userwallet,payment,checkout
#from shop.views.profileview import ProfileList,ProfileRetrieveView
from shop.views.profileview import index,updateDetails
from shop.views.commentview import CommentRetrieveView,CommentList
from email_auth.views import SignUpView,LoginRequest,LogoutRequest
from shop.views.homeview import displayhome







sitemaps = {'cmspages': CMSSitemap,
            'products': ProductSitemap}



def render_robots(request):
    permission = 'noindex' in settings.ROBOTS_META_TAGS and 'Disallow' or 'Allow'
    return HttpResponse('User-Agent: *\n%s: /\n' % permission, content_type='text/plain')

i18n_urls = (
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),


    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/?$',
        PasswordResetConfirm.as_view(template_name='myshop/pages/password-reset-confirm.html'),
        name='password_reset_confirm'),
    url(r'^', include('cms.urls')),
)
urlpatterns = [
    url(r'^robots\.txt$', render_robots),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^multi_form/$', ContactFormAjaxView.as_view(), name='multi_form'),
    url(r'^$', ContactFormView.as_view(), name='contact_form'),
    url(r'^blogging_form/$',BlogFormAjaxView.as_view(),name='blogging_form' ),
    url(r'^$', ProfileFormView.as_view(), name='Profile_Form'),
    url(r'^blogging_form/$',ProfileFormAjaxView.as_view(),name='Profile_form' ),
    url(r'^$', BlogFormView.as_view(), name='Blog_Form'),
    url(r'^contacts/$', CommentList.as_view()),
    url(r'^contacts/(?P<pk>[0-9]+)$', CommentRetrieveView.as_view()),
    url(r'^blogging/$',BlogList.as_view()),
    url(r'^blogging/(?P<pk>[0-9]+)$', BlogRetrieveView.as_view()),
    url(r'^profilelist/$',index,name=''),
    url(r'^profile/(?P<pk>[0-9]+)$', updateDetails,name='profile_with_pk'),
    url(r'^joblist/$',jobindex.as_view(),name='joblist'),
    url(r'^userjoblist/$',JobListing.as_view(),name='joblisting'),
    url(r'^job/(?P<pk>[0-9]+)$', jobupdateDetails,name='job_with_pk'),
    url(r'^job/(?P<pk>[0-9]+)$',displayjob,name='displayjob_with_pk'),
    url(r'^ad-jobs/$',upload,name='upload'),
    url(r'^ad-jobprofile/$',profileupload,name='profileupload'),
    url(r'^ad-profile/$',uploadprofile,name='uploadprofile'),
    url(r'^job/(?P<pk>[0-9]+)/addjobbid/$',addjobbid,name='addjobbid'),
    url(r'^register/signup/$', SignUpView.as_view() ,name='signup'),
    url(r'^register/signup/freelancer/$', freelancerSignUpView.as_view(), name='freelancer_signup'),
    url(r'^register/signup/jobpublisher/$', JobpublisherSignUpView.as_view(), name='jobpublisher_signup'),
    #url(r'^register/signup/teacher/$', TeacherSignUpView, name='teacher_signup'),
    url(r'^login/$', LoginRequest,name='login'),
    url(r'^logout/$', LogoutRequest),
    url(r'^jobbid/(?P<pk>[0-9]+)$', jobbidoffer,name='jobbid_offer_pk'),
    url(r'^usertask/$',Tasklisting.as_view(),name='tasklisting'),
    url(r'^offers/$', offers.as_view(), name='offers'),
    url(r'^offers/(?P<pk>[0-9]+)$', Accepted,name='accepted'),
    url(r'^offers/(?P<pk>[0-9]+)$', Rejected,name='rejected'),
    #url(r'^checkout/(?P<pk>[0-9]+)$', checkout, name='checkout'),
    url(r'^cashwithdraw/$', cashwithdraw.as_view(), name='cashwithdraw'),
    url(r'^success/$', success.as_view(), name='sucess'),
    url(r'^wallet/$',Userwallet,name= 'wallet' ),
    url(r'^checkout/(?P<pk>[0-9]+)$', checkout, name='checkout'),
    url(r'^checkout/payment/(?P<pk>[0-9]+)$', payment, name='payment'),
    url(r'^searching/$',searching,name='search'),
    url(r'^home/$',displayhome.as_view(),name='Home'),
    url(r'^joblist/get_joblist/$', mapsearch, name='get_joblist'),

    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.USE_I18N:
    urlpatterns.extend(i18n_patterns(*i18n_urls))
else:
    urlpatterns.extend(i18n_urls)
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
