# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Place
from .forms import PlaceForm

@login_required
def homepage(request):
    place_list = Place.objects.filter(owner=request.user)
    return render(request, "homepage.html", {
            "place_list" : place_list
        })

@login_required
def add_place(request):
    form = PlaceForm()
    if request.method == "POST" :
        # Kita copy data hasil dari form POST ke names data
        data = request.POST.copy()
        # Masukan data dan juga file gambar yang di upload ke form Place Form.
        # File yang diupload lewat form akan tersedia di names request.FILES
        form = PlaceForm(data, request.FILES)
        if form.is_valid() :
            place = form.save(commit=False)
            place.owner = request.user
            place.save()
            messages.success(request, "Place successfuly added !")
            return redirect("homepage")
        else :
            messages.error(request, form.errors)
    return render(request, "add_place.html", {
            "form" : form
        })

@login_required
def edit_place(request, place_id):
    place = Place.objects.get(id=place_id)
    form = PlaceForm(instance=place)
    if request.method == "POST" :
        data = request.POST.copy()
        form = PlaceForm(data, request.FILES, instance=place)
        if form.is_valid() :
            # Menyimpan ke memory form yang telah di isi dan di validasi
            # tanpa benar-benar menyimpannya ke database
            place = form.save(commit=False)
            # Menambahkan attribute owner ke form yang akan disimpan
            place.owner = request.user
            # Menyimpan nya ke database
            place.save()
            messages.success(request, "Place %s successfuly edited !" % place.name)
            return redirect("homepage")
        else :
            messages.error(request, form.errors)
    return render(request, "editplace.html", {
            "form" : form
        })

@login_required
def delete_place(request, place_id):
    place = Place.objects.get(id=place_id)
    if place.is_active :
        messages.error(request, "Sorry you can't delete active place !")
    else :
        place.delete()
        messages.success(request, "Place successfuly deleted !")
    return redirect("homepage")

@login_required
def detail_place(request, place_id):
    place = Place.objects.get(id=place_id)
    return render(request, "detailpage.html", {
            "place" : place
        })

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
        if user and user.is_staff :
            # Fungsi login digunakan untuk mendaftarkan session untuk object user
            login(request, user)
            messages.success(request, "Hi, welcome again %s" % username )
            return redirect("homepage")
        elif user and not user.is_staff :
            messages.error(request, "You can't access this site !")
        else :
            messages.error(request, "Wrong username or password combination !")
    return render(request, "login.html")

def logoutpage(request):
    logout(request)
    return redirect('loginpage')

def regpage(request):
    if request.method == "POST" :
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        # Kondisi ini memastikan bahwa username yang digunakan belum pernah didaftarkan.
        if User.objects.filter(username=username):
            messages.error(request, "Username %s already exist, please choose another one" % username)
        else :
            # Kondisi ini memastikan bahwa password dan konfirmasi password sama.
            if password1 != password2 :
                messages.error(request, "Password does not match !")
            else :
                user = User.objects.create_user(username, password=password1, is_staff=True)
                login(request, user)
                messages.success(request, "Hi %s , welcome the first time" % username )
                return redirect("homepage")
    return render(request, "reg.html")
