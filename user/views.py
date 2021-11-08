
#----api.py code----
import hashlib

from django.http import QueryDict
from django.views.decorators.http import require_http_methods
from requests import post
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

import json
from socialmedia import *
from .loginSerialization import *
from .serialization import *
from .user_serialization import *
from .OtpSerialization import *

import random,smtplib


#-----------------signup get post put delete-----------------

@api_view(['GET','POST'])
#@csrf_exempt

def users_new2(request):
    print("----------inside user new function")

    form = serializerClass()
    if(request.method == 'GET'):
        print("get getting called")
    #if request.method == 'POST':
        #form = serializerClass(request.POST)
    #    if form.is_valid():
    #        form.save()
    #        return redirect('users_new')
    #if request.is_ajax():
    #user_post_data = JSONParser().parse(request)
    #user_serializer = user_Serialization_Class(data=user_post_data)


    print("req meth: ",request.method,"\nreq post value",request.POST)
    print("req data: ",request.data)
    if request.method=='POST':
        # -----email setup and login---------------------
        number = random.randint(1111, 9999)  # otp generration
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.login('franzosocialmedia@gmail.com', 'apurva87654321')
        print(s.login('franzosocialmedia@gmail.com', 'apurva87654321'))

        print("inside ajax if")
        print("req data post print ----- ",(request.data))
        #print("req data post print iterate ----- ", (request.data['emailid']))    #fetching email id from query dictionary
        copy_GET = QueryDict('a=1&a=2&a=3', mutable=True)
        print("PASS COPYget")
        #l = copy_GET.getlist('a')
        #l.append(u'4')
        #copy_GET.setlist('a', l)
        form = serializerClass(data=request.POST)
        #print("data form variable: ---", type(form))
        #print("type req post ", type(request.POST))
        data_dict = request.data.dict()   #converting query dict to dictionary
        print("type:---------", type(request.POST))
        print("data dict: ",data_dict)
        email_id = data_dict['emailid']

        request.data._mutable = True
        request.data['otp'] = number
        request.data['password']= hashlib.md5(request.data['password'].encode()).hexdigest()
        print("serializer value: ", request.data)

        print("add otp: ", request.data['otp'])

        #serializer = OtpserializerClass(request.POST, data=request.data)
        print("serializer called-------------------------------------")

        if form.is_valid():
            print("inside valid form---###")

            form.save()
            s.sendmail('franzosocialmedia@gmail.com', request.data['emailid'], str(number))

            #print("data form variable: ---", (form))
            return Response(form.data, status=status.HTTP_201_CREATED)

            #print("errors serializer: ",form.errors)
        return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)
    print("\nif not post ")
    return render(request, 'users_new.html', {'form': form})

@api_view(['GET', 'POST'])
def otp(request):
    #getQueryString = request.data.get('emailid')
    #rint("type get qs ", type(getQueryString), "value ", getQueryString)
    #request.data._mutable=True
    print("req data otp ---------->  ", request.data)
    #print("emailId- ",getQueryString)
    #users_new2(request)
    #form = serializerClass(data=request.POST)
    if request.method=='POST':
        print("req data otp : ",request.data," type ",type(request.data))
        form= serializerClass(data= request.POST)
        request.data._mutable=True
        print("otp------>>> ",request.data['otp'])
    #print("type of req data: ",(form))
    #getQueryString = users_new.objects.all # verify otp(naman)
    #form = serializerClass(data=request.POST)
    #getQueryString= request.data['emailid']
    #print("get query string verify : ", getQueryString)
    # print("type pf get query: ",type(getQueryString))
    # print("** query: ", type(**getQueryString))
    #course_qs = users_new.objects.filter(**getQueryString)
    #course_qs = request.session.get(**getQueryString)

    #print("course qs: ", course_qs)
    # print("type of course qs: ", type(course_qs))
    '''if (course_qs.exists()):
        print("\n\n query set verify: ", course_qs)
        print("\n\n query set verify: ", course_qs)
        model = None
        for course in course_qs:
            model = course
        sample = list(course_qs.values_list()[0])
        print("verify sample: ")

        print(sample)  # has the data of the logged in user as a list



        return Response("OTP verified: ", status=status.HTTP_200_OK)

    else:
        return Response("Otp verification fail", status=status.HTTP_400_BAD_REQUEST)  # verify otp end-----
'''
    return render(request, 'signup_otp.html')


#------signup fetch end


def signIn(request):
    return render(request,'sign_in.html')
