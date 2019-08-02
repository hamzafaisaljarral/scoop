from django.http import HttpResponseRedirect
from email_auth.models import User
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.utils.decorators import method_decorator
from email_auth.forms import RegistrationForm, LoginForm


from django.contrib.auth import authenticate, login, logout

from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'myshop/pages/signupsimple.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.Usertype.freelancer:
            return redirect('/joblist/')
        else:
            return redirect('/profilelist/')
    return render(request, 'shop/Homepage/home2.html')






def UserRegistration(request):
        if request.user.is_authenticated():
                return HttpResponseRedirect('/profile/')
        if request.method == 'POST':
                form = RegistrationForm(request.POST)
                if form.is_valid():
                        user = User.objects.create_user(username=form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
                        user.save()
                        user = User(user=user)
                        user.save()
                        return HttpResponseRedirect('/')
                else:
                        return render(request,'myshop/pages/signupsimple.html', {'form': form})
        else:
                ''' user is not submitting the form, show them a blank registration form '''
                form = RegistrationForm()
                context = {'form': form}
                return render(request,'myshop/pages/signupsimple.html', context)

@login_required
def creatuserprofile(request):
        if not request.user.is_authenticated():
                return HttpResponseRedirect('/login/')
        userstype = request.user.get_profile
        if userstype.freelancer == True:
         context= {'userstype' : userstype }
         return HttpResponseRedirect('/ad-profile/')

        if userstype.jopublisher == True:
                context = {'userstype': userstype}
                return HttpResponseRedirect('/ad-jobs/')

        return HttpResponseRedirect('/register/')


def LoginRequest(request):
        if request.user.is_authenticated():
                return HttpResponseRedirect('/home/')
        if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']
                        userstype = authenticate(username=username, password=password)
                        if userstype is not None:
                                login(request, userstype)
                                return HttpResponseRedirect('/home/')
                        else:
                                return render(request, 'myshop/pages/simplelogin.html', {'form': form})
                else:
                        return render(request, 'myshop/pages/simplelogin.html', {'form': form})
        else:
                ''' user is not submitting the form, show the login form '''
                form = LoginForm()
                context = {'form': form}
                return render(request, 'myshop/pages/simplelogin.html', context)


def LogoutRequest(request):
        logout(request)
        return HttpResponseRedirect('/login/')
