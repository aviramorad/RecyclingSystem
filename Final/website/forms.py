from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User

class PrivateSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    location = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.usertype = False
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')  # Fixed typo here
        user.email = self.cleaned_data.get('email')
        user.location = self.cleaned_data.get('location')
        if commit:
            user.save()
        return user

class CorpSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    location = forms.CharField(required=True)
    comp_num = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.usertype = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')  
        user.email = self.cleaned_data.get('email')
        user.location = self.cleaned_data.get('location')
        user.comp_num = self.cleaned_data.get('comp_num')
        if commit:
            user.save()
        return user
