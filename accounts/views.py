from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from accounts.forms import UserForm
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    form = UserForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return HttpResponseRedirect('/')
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        if 'next' in request.POST:
            return HttpResponseRedirect(request.POST.get('next'))
        else:
            return HttpResponseRedirect('/')
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))