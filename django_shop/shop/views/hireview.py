from cms.utils import get_language_from_request
#from django.http import HttpResponse, JsonResponse, Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.parsers import JSONParser
from hire.models import Hire,Subscription
from jobs.models import Jobs,Jobbid,ProfileJob
from wallet.models import Wallet
from rest_framework import mixins
from rest_framework.views import APIView
from shop.serializers.jobsserializer import JobSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import renderers
from rest_framework import viewsets
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from shop.forms.hireform import Hireform
from shop.forms.walletform import Walletform
from shop.forms.applyjobsform import Applyjobsform
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from hire.extra import generate_order_id, transact, generate_client_token
from django.contrib.auth import login
from datetime import date
from dateutil import parser
import os
import random
import logging
import string
from django.shortcuts import render
from django.core.urlresolvers import reverse
from rest_framework.reverse import reverse

from django.core.files.storage import FileSystemStorage
from email_auth.models import User
from django.conf import settings
import braintree
braintree.Configuration.configure(braintree.Environment.Sandbox,
							  merchant_id=settings.BRAINTREE_MERCHANT,
							  public_key=settings.BRAINTREE_PUBLIC_KEY,
							  private_key=settings.BRAINTREE_PRIVATE_KEY)


def jobbidoffer(request, pk):
    jobbid = get_object_or_404(Jobbid, pk=pk)
    if request.method == 'POST':
        form1 = Walletform(request.POST)
        form = Hireform(request.POST)
        if form.is_valid() or form1.is_valid():
            hires = form.save(commit=False)
            hires.hiredprofile = jobbid.Yourprofile
            hires.jobhiredfor = jobbid.jobappliedto
            hires.profileofjobpublisher = request.user.profilejob
            hires.price = jobbid.price
            hires.end_date = jobbid.jobappliedto.end_date
            hires.save()
            wallets = form1.save(commit=False)
            wallets.freelanceprofile = jobbid.Yourprofile
            wallets.jobpaidfor = jobbid.jobappliedto
            wallets.paidby = request.user.profilejob
            wallets.pendingpayment = jobbid.price
            wallets.amount = jobbid.price
            wallets.end_date = jobbid.jobappliedto.end_date
            wallets.save()
            pk = hires.pk
            data=get_object_or_404(Hire, pk=pk)
            #wallet = get_object_or_404(Wallet,pk=pk)
            # jobs = Job.objects.get(pk=pk)
            return HttpResponseRedirect(reverse('checkout', args=(data.id,)))

    else:
        form = Hireform()
        form1 = Walletform()
    return render(request, 'shop/jobsdisplay/addjob.html', {
        'form': form, 'form1':form1
    })



class Tasklisting(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shop/hiredisplay/assigntasks.html'
    model = Hire



    def get(self, request):
     today = date.today()
     queryset = Hire.objects.filter(profileofjobpublisher=request.user.profilejob)
     return Response({'job': queryset,'time':today })



class offers(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shop/Profiles/offersend.html'
    model = Hire

    def get(self, request):
        today = date.today()
        queryset = Hire.objects.filter(hiredprofile=request.user.profile)
        return Response({'job': queryset,'time':today })





def Userwallet(request, totalcost=None):
    today = date.today()
    wallets = Wallet.objects.filter(freelanceprofile=request.user.profile)
    cashout =+ sum(items.amount for items in wallets if items.end_date.year <= today.year and items.end_date.month <= today.month and items.end_date.day <= today.day)
    totalcost = sum(items.pendingpayment for items in wallets)
    return render(request, 'shop/hiredisplay/userwallet.html', {'wallets': wallets,'total':totalcost,'datetoday':today,'cash':cashout })



def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(request.user.profilejob, user=request.user.profilejob)
    order = Jobs.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


def subscription(request):
	rg = request.POST.get
	message = ''
	token = None
	customer_id = None
	if request.POST:
		if rg('fname') and rg('lname') and rg('cnumber') and rg('cvv') and rg('year') and rg('month'):
			#print rg('fname'), rg('lname'), rg('cnumber'), rg('cvv'), rg('year'), rg('month')

            # number = rg('cnumber')
			# expiration_date = rg('year')/rg('month')

			client_token = braintree.ClientToken.generate()

            #print "client_token"
        # result = braintree.Customer.create({
			#     "credit_card": {
			#         "number": "4111111111111111",
			#         "expiration_date": "12/16"
			#       }
			#   })

			# print result

			# print result.customer.payment_method_nonce

			# result = braintree.Subscription.create({
			#     "payment_method_token": result.credit_cards[0].token,
			#     "plan_id": "my_plan_id"
			#   })

			# print
			# if result.is_success:
			#   print "Subscription success!"

			# customer = braintree.Customer.create({
			#     "credit_card": {
			#         "number":number,
			#         "expiration_date":expiration_date,
			#     }
			# })

			# payment_method_token = client.customer.credit_cards[0].token



			# token = client_token()
			# payment_token_id = generate_payment_token(token)
			# print payment_token_id




def client_token():
	 client_token = braintree.ClientToken.generate()
	 return client_token

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def generate_payment_token(token):
	payment_token_nonce = braintree.PaymentMethod.create({
	"customer_id": token,
	"payment_method_nonce": nonce_from_the_client
	})



@login_required
@csrf_exempt
def checkout(request,pk):
	rg = request.POST.get

	amount =  get_object_or_404(Hire, pk=pk)

	#print "============"
	#print amount
	user = ProfileJob.objects.get(name=request.user.profilejob.name)
	a_customer_id = ''
	if not user.customer_id:
		result = braintree.Customer.create({
		    "first_name": user.name,
		    "last_name": "jobpublisher",
		    "company": "Braintree",
		    "email": user.location,
		    "phone": "312.555.1234",
		    "fax": "614.555.5678",
		    "website": "www.example.com"
			})
		if result.is_success:
			user.customer_id = result.customer.id
			user.save()
			a_customer_id = user.customer_id
	else:
		a_customer_id = user.customer_id
	if not user.client_token:
		client_token = client_token = braintree.ClientToken.generate({
			    "customer_id": a_customer_id
			})
		user.client_token = client_token
		user.save()
	else:
		client_token = user.client_token

	varibles ={'amount':amount,'client_token':client_token}
	return render(request, 'shop/hiredisplay/checkout.html',varibles)

@login_required
@csrf_exempt
def payment(request,pk):
    if request.POST:
        if request.POST.get("payment_method_nonce"):
            nonce_from_the_client = request.POST.get("payment_method_nonce")
            hire = get_object_or_404(Hire, pk=pk)
            sub = Subscription()
            sub.hires = hire
            sub.payment_nonce = nonce_from_the_client
            sub.amount = request.POST.get("amount")
            sub.save()
            result = braintree.Transaction.sale({
                "amount": sub.amount,
                "payment_method_nonce": sub.payment_nonce
            })
            transaction_id = result.transaction.id
            sub.txnid = transaction_id
            sub.save()
            message = ''
            if result.is_success:
                sub.result = True
                sub.save()
                message = 'Transaction successfully completed' + ' : ' + transaction_id
                varibles = {'message': message}
                return render(request, 'shop/hiredisplay/purchase_success.html', varibles)
            else:
                message = 'Error Transaction Fail'

                varibles = {'message': message, }
                return render(request, 'shop/hiredisplay/checkout.html', varibles)
        else:
            message = 'No transaction'

            varibles = {'message': message, }
            return render(request, 'shop/hiredisplay/checkout.html', varibles)


class cashwithdraw(generics.GenericAPIView):
        renderer_classes = [TemplateHTMLRenderer]
        template_name = 'shop/hiredisplay/cashwithdraw.html'
        model = Hire

        def get(self, request):
            queryset = Hire.objects.filter(hiredprofile=request.user.profile)
            return Response({'job': queryset})


class success(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shop/hiredisplay/purchase_success.html'
    model = Hire

    def get(self, request):
        queryset = Hire.objects.filter(hiredprofile=request.user.profile)
        return Response({'job': queryset})


def Accepted(request, pk):
   emp = Hire.objects.get(pk = pk)
   #you can do this for as many fields as you like
   #here I asume you had a form with input like <input type="text" name="name"/>
   #so it's basically like that for all form fields
   emp.is_accepted = 'True'
   emp.save()
   return redirect('offers')

def Rejected(request, pk):
   emp = Hire.objects.get(pk = pk)
   #you can do this for as many fields as you like
   #here I asume you had a form with input like <input type="text" name="name"/>
   #so it's basically like that for all form fields
   emp.is_rejected = 'True'
   emp.save()
   return redirect('offers')







