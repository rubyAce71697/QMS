from django.contrib.auth.forms import User
from django import forms
from .models import StudentProfile
from django.utils import six


class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)


    class Meta:
        model = User
        fields = ('username','email','password')


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'password')









    
