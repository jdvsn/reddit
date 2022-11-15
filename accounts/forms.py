from django import forms
from django.contrib.auth.forms import UserCreationForm  

class UserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        label='',
        min_length='3',
        max_length='20')
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email Address'}),
        label='')
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), 
        label='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label='') 