from django.shortcuts import render, get_object_or_404  # render page, return data or 404 page
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth

def login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/clients/')
        else:
            login_error = 'Неверный логин или пароль'
            context = {'login_error': login_error}
            return render(request, 'accounts/login.html', context)
    else:
        return render(request, 'accounts/login.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')