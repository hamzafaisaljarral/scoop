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
from wallet.models import Wallet
from shop.forms.walletform import Walletform
from django.contrib import messages
from email_auth.models import User

#@method_decorator([login_required,freelancer_required], name='dispatch')







@login_required
def uploadprofile(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.account = request.user
            profile.save()
            pk=profile.pk
            profiles = Profile.objects.get(pk=pk)
            return redirect("profile_with_pk", pk , permanent=True)
    else:
        form = ProfileForm()
    return render(request, 'shop/Profiles/createprofile.html', {
        'form': form
    })


def updateDetails(request, pk):
    profiles = Profile.objects.get(pk=pk)
    return render(request, 'shop/Profiles/displayprofile.html', {'profiles': profiles, 'pk': pk})

def index(request):
    profiles = Profile.objects.all()
    profile = Profile.objects
    return render(request, 'shop/Profiles/profilelist.html', {'profiles': profiles, 'profile': profile})

class ProfileList(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shop/Profiles/displayprofile.html'
    model = Profile

    def get(self, request):
      queryset = Profile.objects.all()
      return Response({'profile': queryset})



class ProfileRetrieveView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    queryset = Profile.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'profile': self.object}, template_name='shop/Profiles/displayprofile.html')


class freelancerSignUpView(CreateView):
    model = User
    form_class = FreelancerSignUpForm
    template_name = 'shop/Profiles/createprofile.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'freelancer'
        return super(freelancerSignUpView,self).get_context_data(**kwargs)

    def form_valid(self, form):
        User = form.save()
        login(self.request, User, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('uploadprofile')


