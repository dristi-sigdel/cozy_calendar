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

            # auth_token = str(uuid.uuid4())
            # profile_obj = Profile.objects.create(user = myuser, auth_token = auth_token )
            # profile_obj.save()
            # send_mail_after_registration(email, auth_token)
            # return redirect('/token')
        messages.success(request, "Registered Successfully!")
        return redirect('/info')

        # except Exception as e:
            # print(e)
            
        # messages.success(request, "Successfully Registered!")
    else:
        return render(request, 'users/register.html')

    # else:
        #   return HttpResponse('404 - Not Found')
        

    
# def send_mail_after_registration(email, token):
#     subject = 'Your accounts need to be verified'
#     message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
#     email_from = settings.EMAIL_HOST_USER
#     recepient_list = [email]
#     send_mail(subject, message, email_from, recepient_list)


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

        # if User.objects.filter(age):
        #     messages.error(request, "Should have 0 or more.")
        #     return redirect('/info')

        # if User.objects.filter(days):
        #     messages.error(request, "Should have 0 or more.")
        #     return redirect('/info')

        # if User.objects.filter(cycle):
        #     messages.error(request, "Should have 10 or more.")
        #     return redirect('/info')

        inf = Info(name=name, age=age, days=days, cycle=cycle)
        # print("Hey!")
        inf.save()


        
        len = float(cycle)
        CycleNumber = 1
        LengthofLutealPhase = math.floor((50/100)*len)
        FirstDayofHigh = math.ceil((36/100)*len)
        TotalNumberofHighDays = math.floor((14/100)*len)
        print(LengthofLutealPhase)
        

        # filename = 'model.joblib'
        # track = joblib.load(filename)

        track = pickle.load(open('regr.pkl', 'rb'))
        # print(track)

        df = pd.DataFrame({"CycleNumber":CycleNumber,
                  "ReproductiveCategory": age,
                  "LengthofLutealPhase": LengthofLutealPhase,
                  "FirstDayofHigh": FirstDayofHigh,
                  "TotalNumberofHighDays": TotalNumberofHighDays}, index=[0])

        # print(df)
        

        # arr = []

        # arr.append(CycleNumber)
        # arr.append(LengthofLutealPhase)
        # arr.append(FirstDayofHigh)
        # arr.append(TotalNumberofHighDays)
        # arr.append(age)
        
        # df = pd.DataFrame({"CycleNumber":CycleNumber,
        #           "ReproductiveCategory": age,
        #           "LengthofLutealPhase": LengthofLutealPhase,
        #           "FirstDayofHigh": FirstDayofHigh,
        #           "TotalNumberofHighDays": TotalNumberofHighDays}, index=[0])

        # print(df)
        # result = 29
        # print(result)
                  

        # arr = [CycleNumber, LengthofLutealPhase, FirstDayofHigh, TotalNumberofHighDays, age]
        # arr = np.array(arr)
        # print(arr)
        # arr = arr.reshape(1,-1)
        y_pred = track.predict(df)
        prediction = math.floor(y_pred)
        # print(prediction)
        data=prediction
        # print(y_pred)

        # output = """Menstruation Period in {{prediction}}days"""
        # template =  Template(output)
        # result = template.render
        # return HttpResponse(result)

        # return redirect('/index', {'data': data}) 
        return render(request, 'users/index.html', {'data': data})
        # return redirect("/index", {'data':data})
        # return render(request, 'users/index.html')
    else:
        return render(request, 'users/info.html')
        # messages.error(request, "Invalid Credentials, Please Try Again!")


# def info(request):
#     my_form = InfoForm(request.GET)
#     if request.method == "POST":
#         my_form = InfoForm(request.POST)
#         if my_form.is_valid():
#             Info.objects.create(**my_form.cleaned_data)
#             return redirect("/index")

#     context = {"form": my_form}
#     return render(request, "users/info.html", context)

# def tracker(request):

#     if request.method == 'POST':

#         name = request.POST.get['name']
#         age = request.POST.get['age']
#         days = request.POST.get['days']
#         cycle = request.POST.get['cycle']

#         CycleNumber = 1
#         LengthofLutealPhase = math.floor((50/100)*cycle)
#         FirstDayofHigh = math.ceil((36/100)*cycle)
#         TotalNumberofHighDays = math.floor((14/100)*cycle)
#         print(LengthofLutealPhase)

#         filename = 'model.joblib'
#         track = joblib.load(filename)


#         # def functions():
#         #     data = request.POST.get('cycle')
            
#         #     return (CycleNumber, LengthofLutealPhase, FirstDayofHigh, TotalNumberofHighDays)

#         # track = pickle.load(open('UserManagement/static/ml/regr.pkl', 'rb'))

#         y_pred = track.predict([CycleNumber, LengthofLutealPhase, FirstDayofHigh, TotalNumberofHighDays, age])
#         print(y_pred)
#         return render(request, 'index.html', {'result': 29})
        # fs = FileSystemStorage()
        # filename = fs.save()


        # return render(request, 'index.html')
def profile(request):
    info = Info.objects.all()
    return render(request, "users/Profile.html", {'info':info})

