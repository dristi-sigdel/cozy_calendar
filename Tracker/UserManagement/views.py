from email import message
import pickle
import re
import math
from unittest import result
from django import templatetags
from django.template import Template
import uuid
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as dj_login
from UserManagement.models import Info
import numpy as np
import pandas as pd
from .models import *
from django.conf import settings
from django.core.mail import send_mail

# from sklearn.externals import joblib
import pickle
# readmodel = pickle.load('.\ml\tr')

def home(request):
    return render(request, 'users/home.html')

def bot(request):
    return render(request, 'users/bot.html')


def index(request):
    return render(request, 'users/index.html')

def token(request):
    return render(request, 'users/token.html')

def success(request):
    return render(request, 'users/success.html')


def register(request):
    if request.method == "POST":
        # Get the parameters
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check for the invalid inputs
        # try:
        if len(username) > 20:
            messages.error(request, "SignUp Unsuccessful Username should be under 20 characters !!")
            return redirect('/register')

        if not username.isalnum():
            messages.error(request, "Username should only have letters & numbers")
            return redirect('/register')

        if User.objects.filter(username=username).first():
            messages.error(request, "This username is already taken")
            return redirect('/register')

        if User.objects.filter(email=email).first():
            messages.error(request, "This email is already taken")
            return redirect('/register')

        if re.search('[0-9]', password1) is None:
            messages.error(request, "The password should have a number in it")
            return redirect('/register')

        if len(password1) <= 7:
            messages.error(request, "Password should have atleast 8 characters!!")
            return redirect('/register')

        # CHeck for enourmous inputs
        if password1 != password2:
            messages.error(request, "Password Do not match")
            return redirect('/register')

        myuser = User.objects.create_user(username, email, password1)
        myuser.save()
        messages.success(request, "Registered Successfully!")
        return redirect('/info')

    else:
        return render(request, 'users/register.html')


def login(request):
    if request.method == 'POST':
        # Get POST Parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            dj_login(request, user)
            messages.success(request, "Successfully Logged In!")
            return redirect('/index')
    else:
        # messages.error(request, "Invalid Credentials, Please Try Again!")
        return render(request, 'users/login.html')

def handleLogout(request):
    # if request.method == 'POST':
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('/')
#
#         return HttpResponse('handleLogout')


def info(request):
    if request.method == "POST":
        # Get the parameters
        name = request.POST['name']
        age = request.POST['age']
        days = request.POST['days']
        cycle = request.POST['cycle']
        print(name, age, days, cycle)

        inf = Info(name=name, age=age, days=days, cycle=cycle)
        # print("Hey!")
        inf.save()


        
        len = float(cycle)
        CycleNumber = 1
        LengthofLutealPhase = math.floor((50/100)*len)
        FirstDayofHigh = math.ceil((36/100)*len)
        TotalNumberofHighDays = math.floor((14/100)*len)
        print(LengthofLutealPhase)
        

        track = pickle.load(open('regr.pkl', 'rb'))
        # print(track)

        df = pd.DataFrame({"CycleNumber":CycleNumber,
                  "ReproductiveCategory": age,
                  "LengthofLutealPhase": LengthofLutealPhase,
                  "FirstDayofHigh": FirstDayofHigh,
                  "TotalNumberofHighDays": TotalNumberofHighDays}, index=[0])

        y_pred = track.predict(df)
        prediction = math.floor(y_pred)
        # print(prediction)
        data=prediction


        # return redirect('/index', {'data': data}) 
        return render(request, 'users/index.html', {'data': data})

    else:
        return render(request, 'users/info.html')
        # messages.error(request, "Invalid Credentials, Please Try Again!")

def profile(request):
    info = Info.objects.all()
    return render(request, "users/Profile.html", {'info':info})

