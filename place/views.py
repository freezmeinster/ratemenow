# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

def homepage(request):
    return render(request, "homepage.html")

def loginpage(request):
    # Kondis ini memastikan apabila user sudah login dan mengakses fungsi ini maka
    # akan di-redirect ke homepage
    if request.user.is_authenticated() :
        return redirect("homepage")
    if request.method == "POST" :
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Fungsi authenticate akan menerima paremeter username dan password
        # apabila username dan password cocok makan fungsi ini akan mengembalikan object user
        user = authenticate(username=username, password=password)
        if user :
            # Fungsi login digunakan untuk mendaftarkan session untuk object user
            login(request, user)
            messages.success(request, "Hi, welcome again %s" % username )
            return redirect("homepage")
        else :
            messages.error(request, "Wrong username or password combination !")
    return render(request, "login.html")

def logoutpage(request):
    logout(request)
    return redirect('loginpage')