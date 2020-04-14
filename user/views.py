from django.shortcuts import render
from django.db import IntegrityError
# Create your views here.

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework import generics
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import json
import pickle
import random
from covid_response.settings import BASE_DIR
import os
import string , random
import requests
import re
import os.path
import datetime
from os import path
import bs4
from bs4 import BeautifulSoup
from .models import User,UserDetail,Shop,Slots
from user.serializers import ShopSerializer

a = os.path.join(BASE_DIR, 'static/fixtures/model_output.pkl')
b = os.path.join(BASE_DIR, 'static/fixtures/intent.json')

file = open(a, 'rb')
text_clf = pickle.load(file)
file.close()

with open(b) as f:
    doc7 = f.read()
    inte = json.loads(doc7)
    list_of_intents = inte["intents"]


def getResponse(ints):
    if ints == "noidea":
        result = "I don't get it please ask something related to topic"
    else:
        for i in list_of_intents:
            if i["tag"] == ints:
                result = random.choice(i["responses"])
                break
    return result


def chatbot_response(text):
    a = text_clf.predict_proba([text])
    print(max(a[0]))
    if max(a[0]) < 0.5:
        pred = ["noidea"]
    else:
        pred = text_clf.predict([text])
    res = getResponse(pred[0])
    return res

def registeruser(post_info):
    try:
        reg_email=post_info["email"]
        reg_pass=post_info["pass"]
        reg_fname=post_info["fname"]
        reg_lname=post_info["lname"]
        reg_phno=post_info["phno"]
        reg_sex=post_info["sex"]
        akey = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 16))
        uobj=User(email=reg_email, activation_key=akey,password=reg_pass) 
        uobj.save()
        udobj=UserDetail(fname=reg_fname,lname=reg_lname,phno=reg_phno,sex=reg_sex)
        udobj.uid=uobj
        udobj.save()
        reg_mes="REGISTRATION SUCCESS"   
        return reg_mes
    except IntegrityError as e:
        reg_mes="duplicate email"
        return reg_mes
    
def loginuser(post_info):
    log_email=post_info["email"]
    log_pass=post_info["pass"]
    try:
        realuser=User.objects.get(email=log_email)
        if log_pass==realuser.password:
            log_mes="LOGIN SUCCESS"
        else:
            log_mes="Incorrect Password"   
        return log_mes
    except User.DoesNotExist:
        log_mes="Incorrect Email"
        return log_mes    

def generate_slot(start_time, end_time):
    t = start_time
    while t <= end_time:
        yield t.strftime('%H:%M')
        t = (datetime.datetime.combine(datetime.date.today(), t) +
             datetime.timedelta(minutes=15)).time()

def available_slot(given_time,given_shop_id,given_date):
    slots_booked=Slots.objects.filter(shopid=given_shop_id,slot_date=given_date,slot_time=given_time).count()
    if slots_booked>=5:
        a="NO"
        return a
    else:
        a="YES"
        return a    
        

@csrf_exempt
def shop_list():
    shops = Shop.objects.all()
    serializer = ShopSerializer(shops, many=True)
    return JsonResponse(serializer.data, safe=False)

def confirm_slot(post_info):
    g_shop_id=post_info["shop_id"]
    c_shop_id=int(g_shop_id)
    c_slot_time=post_info["slot_time"]
    g_user_id=post_info["user_id"]
    c_phno=post_info["phno"]
    slot=Slots(shopid=Shop.objects.get(shopid=c_shop_id),slot_time=c_slot_time,user_id=User.objects.get(email=g_user_id),user_phno=c_phno)
    slot.save()
    mess=slot.id
    return mess


class SlotConfirmAPI(APIView):
    def post(self,request,format='json'):
        post_info=json.loads((request.body).decode('utf-8'))
        slot_mess=confirm_slot(post_info)
        return JsonResponse(slot_mess,safe=False) 

            

class ShopListAPI(APIView):
    def post(self,request,format='json'):
        json=shop_list()
        return json

class SlotCheckAPI(APIView):
    def post(self,request,format='json'):
        post_info=json.loads((request.body).decode('utf-8'))
        g_shop_id=post_info["shop_id"]
        g_year=post_info["year"]
        g_month=post_info["month"]
        g_day=post_info["day"]
        start_time=datetime.time(9,00,00)
        end_time=datetime.time(20,00,00)
        slot_generator=generate_slot(start_time ,end_time)
        slot_list=list(slot_generator)
        g_date=datetime.date(g_year,g_month,g_day)
        g_new=int(g_shop_id)
        for i in slot_list:
            a=available_slot(i,g_new,g_date)
            if(a=="NO"):
                slot_list.remove(i)
        key_list=list(range(len(slot_list)))
        slot_dict=dict(zip(key_list,slot_list))
        return JsonResponse(slot_dict,safe=False)

    
class LoginAPI(APIView):
    def post(self,request,format='json'):
        try:
            post_info=json.loads((request.body).decode('utf-8'))
            log_mes=loginuser(post_info)
            return JsonResponse(log_mes,safe=False) 
        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
    
class RegistrationAPI(APIView):
    def post(self,request,format='json'):
        try:
            post_info=json.loads((request.body).decode('utf-8'))
            reg_mes=registeruser(post_info)
            return JsonResponse(reg_mes,safe=False)
        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
 

class FakeNewsChatBotAPI(APIView):
    def post(self, request, format='json'):
        try:
            re = json.loads((request.body).decode('utf-8'))
            ques = re["question"]
            res = chatbot_response(ques)
            return JsonResponse(res, safe=False)
        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


class CovidUpdatesAPI(APIView):
    def post(self, request, format='json'):
        try:
            res = scrape_now()
            return JsonResponse(res, safe=False)
        except ValueError as e:
            return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


def get_contents():
    url = "https://www.mohfw.gov.in/"
    r = requests.get(url)
    txt = ""
    if r.status_code == 200:
        txt = r.text
        return txt


def scrape_now():
    output_json = {
        'Status': '',
        'Message': '',
        'overview': {},
        'state_wise_list': []
    }
    txt = get_contents()
    # get to parsing
    soup = BeautifulSoup(txt, 'html.parser')
    output_json['overview'] = {
        'active': soup.find_all('div', class_="info_label")[1].parent.find('span', class_="icount").next_element,
        'discharged': soup.find_all('div', class_="info_label")[2].parent.find('span', class_="icount").next_element,
        'deaths': soup.find_all('div', class_="info_label")[3].parent.find('span', class_="icount").next_element,
        'migrated': soup.find_all('div', class_="info_label")[4].parent.find('span', class_="icount").next_element,
    }
    tables = soup.find_all('tbody')
    if len(tables) > 0:
        table = tables[9]
        first_row = False
        for tr in list(table.children):
            if isinstance(tr, bs4.element.Tag):
                if first_row:
                    first_row = False
                    continue
                tds = list(tr.children)
                if len(tds) > 1:
                    pass
                else:
                    continue
                if "Total number of confirmed cases in India" == tds[1].get_text():
                    continue
                state = (tds[3]).get_text()
                state = state.replace("Union Territory of ", "")
                state = state.strip()

                data = {}
                data["state_name"] = state
                data["confirmed"] = int((tds[5]).get_text())
                data["foreign"] = int((tds[7]).get_text())
                data["cured"] = int((tds[9]).get_text())
                data["deaths"] = int((tds[11]).get_text())
                output_json['state_wise_list'].append(data)
        output_json['Status'] = 'Success'
        output_json['Message'] = 'Data fetched successfully.'
    else:
        message = message + " ERROR: No Table found \n"
        print("No Table found")
        output_json['Status'] = 'Failure'
        output_json['Message'] = 'No data present.'
    return output_json
