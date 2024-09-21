from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import Order


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Firstname'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Lastname'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    password1 =  forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    password2 =  forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        
        

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class UploadForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['file', 'turnaround', 'verbatim', 'rush']    