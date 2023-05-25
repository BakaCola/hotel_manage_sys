from django.forms import forms
from django.shortcuts import render

from hotel.models import Account


# Create your views here.


class AccountModelForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = "__all__"





