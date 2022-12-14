from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control bg-textbox border border-border text-body',
            }),
        label='',
        min_length='3',
        max_length='20')
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Email Address',
            'class': 'form-control bg-textbox border border-border text-body',
            }),
        label='')
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control bg-textbox border border-border text-body',
            }), 
        label='')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control bg-textbox border border-border text-body',
            }),
        label='') 

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control bg-textbox border border-border text-body',
            }),
        label='',
        min_length='3',
        max_length='20')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control bg-textbox border border-border text-body',
            }), 
        label='')