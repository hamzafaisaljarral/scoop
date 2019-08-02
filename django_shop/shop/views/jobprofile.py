from cms.utils import get_language_from_request
#from django.http import HttpResponse, JsonResponse, Http404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.utils.text import smart_split
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.parsers import JSONParser
from jobs.models import Jobs,Jobbid,ProfileJob
from hire.models import Hire
from rest_framework import mixins
from rest_framework.views import APIView
from shop.serializers.jobsserializer import JobSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from shop.forms.Jobform import JobForm,JobpublisherSignUpForm,JobProfileForm
from shop.forms.applyjobsform import Applyjobsform
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth import login
import os
from rest_framework.reverse import reverse
from django.core.files.storage import FileSystemStorage
from email_auth.models import User








def Applyjob(request):
    if request.method == 'POST':
        form = Applyjobsform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('joblist')
    else:
        form = Applyjobsform()
    return render(request, 'shop/jobsdisplay/applyjobsform.html', {
        'form': form
    })





def upload(request):

        if request.method == 'POST':
            form = JobForm(request.POST, request.FILES)
            if form.is_valid():
                Jobs = form.save(commit=False)
                Jobs.jobprofile = request.user.profilejob
                Jobs.save()
                #pk = job.pk
                #jobs = Job.objects.get(pk=pk)
                return redirect('joblisting')

        else:
            form = JobForm()
        return render(request, 'shop/jobsdisplay/addjob.html', {
            'form': form
        })

def profileupload(request):
    if request.method == 'POST':
        form = JobProfileForm(request.POST, request.FILES)
        if form.is_valid():
            ProfileJob = form.save(commit=False)
            ProfileJob.account = request.user
            ProfileJob.save()
            #pk = ProfileJob.pk
            #jobs = ProfileJob.objects.get(pk=pk)
            return redirect('upload')

    else:
        form = JobProfileForm()
    return render(request, 'shop/jobsdisplay/addjob.html', {
        'form': form
    })

def displayjob(request,pk):
    jobs = Jobs.objects.get(pk=pk)
    return render(request, 'shop/jobsdisplay/displayjob.html', {'jobs': jobs, 'pk': pk})



def jobupdateDetails(request, pk):
   jobs = Jobs.objects.get(pk=pk)
   hiring = Hire.objects.all()
   form = Applyjobsform()
   return render(request, 'shop/jobsdisplay/jobdetail.html', {'hiring': hiring ,'jobs': jobs, 'form': form})



def addjobbid(request, pk):
    jobs = get_object_or_404(Jobs, pk=pk)
    form = Applyjobsform(request.POST)
    if form.is_valid():
        price = form.cleaned_data['price']
        details = form.cleaned_data['Details']
        #user_name = form.cleaned_data['Yourprofile']
        jobbid = Jobbid()
        jobbid.jobappliedto = jobs
        jobbid.Yourprofile = request.user.profile
        jobbid.price = price
        jobbid.Details = details
        jobbid.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('job_with_pk', args=(jobs.id,)))
    #jobbid = Jobbid.objects.all()
   #jobbid_filter = dateFilter(request.Get, queryset=jobbid)

    return render(request, 'shop/jobsdisplay/jobdetail.html', {'job': jobs, 'form': form})
    #jobs = Job.objects.get(pk=pk)
    #return render(request, 'shop/jobsdisplay/jobdetail.html', {'jobs': jobs, 'pk': pk})





class jobindex(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shop/jobsdisplay/joblist.html'
    model = Jobs

    def get(self,request):
        job = Jobs.objects.all()
        location_contain_query = self.request.GET.get('input')
        if location_contain_query != '' and location_contain_query is not None:
            job = job.filter(location__istartswith=location_contain_query)
        else:
            job = job.filter(location__icontains = 'washington')

        return Response({'job': job,'enterval':location_contain_query})

def mapsearch(request):
    location_contain_query = request.GET.get('inputValue')
    print(location_contain_query)
    if location_contain_query != '' and location_contain_query is not None:
        jobs = Jobs.objects.filter(location__istartswith=location_contain_query).values()
        job_list = list(jobs)

    return JsonResponse(job_list,safe=False)



def searching(request):

    jobs = Jobs.objects.filter(location=request.user.profile.location)
    job = Jobs.objects
    return render(request, 'shop/jobsdisplay/searchresult.html', {'jobs': jobs, 'job': job})



class ProfileList(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shop/Profiles/displayprofile.html'
    model = Jobs

    def get(self, request):
      queryset = Jobs.objects.all()
      return Response({'job': queryset})

class JobListing(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shop/jobsdisplay/jobpublisherprofile.html'
    model = Jobs

    def get(self, request):
      queryset = Jobs.objects.filter(jobprofile=request.user.profilejob)
      return Response({'job': queryset})

class ProfileRetrieveView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):

    queryset = Jobs.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'profile': self.object}, template_name='shop/Profiles/displayprofile.html')


class JobpublisherSignUpView(CreateView):
    model = User
    form_class = JobpublisherSignUpForm
    template_name = 'shop/jobsdisplay/addjob.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'jopublisher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        User = form.save()
        login(self.request, User, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('profileupload')

