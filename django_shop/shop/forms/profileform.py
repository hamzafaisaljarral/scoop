from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from email_auth.models import User

from profile.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        name = forms.CharField(

            widget=forms.TextInput(

            )
        )
        description = forms.CharField(

            widget=forms.TextInput(

            )
        )
        skills = forms.CharField(

            widget=forms.Textarea(

            )
        )

        DOB = forms.DateField(

            widget=forms.DateField(

            )

        )
        phonenumber = forms.IntegerField(

            widget=forms.NumberInput(

            )

        )


        organization = forms.CharField(  max_length=30,
            widget=forms.Textarea(

            )
         )
        location = forms.CharField(

            widget=forms.Textarea(),
            help_text='Write location!'
        )
        price = forms.IntegerField(

            widget=forms.IntegerField(),

        )


        fields = ['name', 'description','location','DOB','skills','price','webpage','organization','phonenumber','profileimage','samplework1','samplework2','samplework3','samplework4']
        required_fields = ['name', 'description','location','DOB','skills','price','webpage','organization','phonenumber','samplework1','samplework2','samplework3','samplework4' ]

        def __init__(self, user, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)
            self.fields['account'].queryset = Profile.objects.filter(account=user)

class FreelancerSignUpForm(UserCreationForm):




            class Meta(UserCreationForm.Meta):
                model = User

            @transaction.atomic
            def save(self):
                User = super().save(commit=False)
                User.freelancer = True
                User.save()
                #profile = Profile.objects.create(account=User)



                return User


