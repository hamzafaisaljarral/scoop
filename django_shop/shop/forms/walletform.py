from django import forms

from wallet.models import Wallet


class Walletform(forms.ModelForm):
    class Meta:
       model = Wallet

       exclude = {'jobpaidfor','freelanceprofile','paidby','pendingpayment','amount','project_end_date',}




