from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from email_auth.models import User

from jobs.models import Jobs,ProfileJob
from . import widgets
from django.forms import DateInput

class JobProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileJob
        name = forms.CharField(

            widget=forms.TextInput(

            )
        )
        aboutyou = forms.CharField(

            widget=forms.TextInput(

            )
        )

        address = forms.CharField(  max_length=30,
            widget=forms.Textarea(

            )
         )
        location = forms.CharField(

            widget=forms.Textarea(),
            help_text='Write location!'
        )


        fields = ['name', 'address','location','aboutyou','profileimage']
        required_fields = ['name', 'address','location','aboutyou','profileimage']

        def __init__(self, user, *args, **kwargs):
            super(JobProfileForm, self).__init__(*args, **kwargs)
            self.fields['account'].queryset = ProfileJob.objects.filter(account=user)
            self.fields['name'].required = True
            self.fields['aboutyou'].required = True
            self.fields['profileimage'].required = True
            self.fields['address'].required = True
            self.fields['location'].required = True



class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs

        fields = ['type', 'location','title','start_date','end_date','price','description','images']
        widgets = {
            'end_date': DateInput(attrs={'type': 'date'}),
            'start_date':DateInput(attrs={'type':'date'}),
        }

        required_fields = ['type', 'location','title','start_date','end_date','price','description','images' ]








class JobpublisherSignUpForm(UserCreationForm):
            class Meta(UserCreationForm.Meta):
                model = User

            @transaction.atomic
            def save(self):
                User = super().save(commit=False)
                User.jopublisher = True
                User.save()
                # profile = Profile.objects.create(account=User)

                return User
