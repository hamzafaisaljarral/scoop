from cms.utils import get_language_from_request
from django.db import transaction
from django.http import HttpResponse, JsonResponse, Http404,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from django.contrib.auth import login
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.parsers import JSONParser
from profile.models import Profile
from jobs.models import Jobs,Jobbid,ProfileJob
from django.db.models import Q
from shop.forms.profileform import ProfileForm,FreelancerSignUpForm
from rest_framework import mixins
from rest_framework.views import APIView
from shop.serializers.profileserializer import ProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.db import transaction
import os
from rest_framework.reverse import reverse

from django.contrib import messages
from email_auth.models import User

#@method_decorator([login_required,freelancer_required], name='dispatch')



class displayhome(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shop/Homepage/home2.html'
    model = Profile

    def get(self,request):
      queryset = Profile.objects.all()
      queryset2 = Jobs.objects.all()
      title_contain_query = self.request.GET.get('title')
      location_contain_query = self.request.GET.get('location')

      if title_contain_query != '' and title_contain_query is not None:
          queryset2 = queryset2.filter(type__icontains=title_contain_query)
      elif location_contain_query != '' and location_contain_query is not None:
          queryset2 = queryset2.filter(location__icontains=location_contain_query)
      return Response({'profile': queryset, 'jobs' : queryset2})





