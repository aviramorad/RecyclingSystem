from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django import forms
from django.db import transaction
from .models import User, products, usersrecycling,ShopForm
from django.utils.translation import gettext_lazy as _

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
        user.user_type = 0
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')  
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
        user.user_type = 1
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')  
        user.email = self.cleaned_data.get('email')
        user.location = self.cleaned_data.get('location')
        user.comp_num = self.cleaned_data.get('comp_num')
        if commit:
            user.save()
        return user
    

class ProductForm(forms.ModelForm):
    class Meta:
        model = products
        fields = ["id", "product_name", "value", "bin_type"]
        labels = {
            "id": _("מזהה"),
            "product_name": _("שם מוצר"),
            "value": _("נקודות"),
            "bin_type": _("סוג פח"),
        }
        widgets = {
            'value': forms.TextInput(attrs={'readonly': True}),
        }


class storeProductForm(forms.ModelForm):
    class Meta:
        model = products
        fields = ["id", "product_name", "value"]
        labels = {
            "id": _("מזהה"),
            "product_name": _("שם מוצר"),
            "value": _("מחיר"),
    }
    
    def __init__(self, *args, **kwargs):
        super(storeProductForm, self).__init__(*args, **kwargs)


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "location", "comp_num", "points"]
        labels = {
            "id": _("מזהה"),
            "username": _("שם משתמש"),
            "first_name": _("שם פרטי"),
            "last_name": _("שם משפחה"),
            "email": _("אימייל"),
            "location": _("עיר מגורים"),
            "comp_num": _("ח.פ"),
            "points": _("הנקודות שלי"),
        }
        help_texts = {
            'username': '',
        }
    def __init__(self, *args, **kwargs):
        super(UserDetailsForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['readonly'] = True
        
class UserDetailsEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "password", "email", "location", "comp_num"]
        widgets = {
            'username': forms.TextInput(attrs={'readonly': True}),
            'password': forms.PasswordInput(),
        }
        labels = {
            "id": _("מזהה"),
            "username": _("שם משתמש"),
            "first_name": _("שם פרטי"),
            "last_name": _("שם משפחה"),
            "password": _("סיסמה"),
            "email": _("אימייל"),
            "location": _("עיר מגורים"),
            "comp_num": _("ח.פ"),
        }
        help_texts = {
            'username': '',
        }
    def clean_password(self):
        # Hash the password before saving
        password = self.cleaned_data.get('password')
        if password:
            return make_password(password)
        return password
class UserRecyclingForm(forms.ModelForm):
    class Meta:
        model = usersrecycling
        fields = ["product", "userImg"]
        labels = {
            "product": _("בחר מוצר למיחזור"),
            "userImg": _("העלאת תמונה"),
        }

    def __init__(self, *args, **kwargs):
        super(UserRecyclingForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = products.objects.filter(Product_type=False)


class shopDigital(forms.ModelForm):
    class Meta:
        model = products
        fields = ["id", "product_name", "Product_type", "value", "bin_type"]
        labels = {
            "id": _("מזהה"),
            "product_name": _("שם מוצר"),
            "Product_type": _("סוג מוצר"),
            "value": _("מחיר/נקודות"),
    }
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['bin_type'].required = True