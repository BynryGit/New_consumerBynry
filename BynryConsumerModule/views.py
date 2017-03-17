from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib import auth
import urllib
import smtplib
from smtplib import SMTPException
from django.shortcuts import *
from BynryConsumerModuleapp.models import Zone,BillCycle,RouteDetail,Branch,SystemUserProfile,City,UserRole,Branch
import json
import traceback
import datetime
from consumerapp.views import get_city

# importing mysqldb and system packages
import MySQLdb, sys
from django.db.models import Q
from django.db.models import F
from django.db import transaction
import pdb

# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect



def dashboard(request):
    return render(request, 'dashboard.html')

def system_user(request):
    data = {
            'city_list': get_city(request),
        }
    return render(request, 'system_user.html',data)

def administrator(request):
    return render(request, 'administrator.html')

def complaints(request):
    return render(request, 'complaints.html')

def services(request):
    return render(request, 'services.html')

#vigilance_cases
def vigilance_cases(request):
    return render(request, 'vigilance_cases.html')
       
def payments(request):
    return render(request, 'payments.html')

def save_system_user_details(request):
    try:
        print 'views.py|save_head_admin_details'
        city_obj = City.objects.get(city=request.GET.get('city'))
        role_obj = UserRole.objects.get(role=request.GET.get('role'))
        user_obj = SystemUserProfile(
            username=request.GET.get('email'),
            password=request.GET.get('password'),
            contact_no=request.GET.get('contact_no'),
            first_name=request.GET.get('first_name'),
            last_name=request.GET.get('last_name'),
            city=city_obj,
            employee_id=request.GET.get('emp_id'),
            role=role_obj,
            email=request.GET.get('email'),
            status=request.GET.get('user_status'),
            )
        user_obj.save()
        if request.GET.get('branch'):
            branch_obj = Branch.objects.get(branch_name=request.GET.get('branch'))
            user_obj.branch = branch_obj
            user_obj.save()
        data={'success':'True'}

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|save_system_user_details', e
        print 'Exception', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_system_user_details(request):
    try:
        print 'views.py|get_system_user_details'
        user_obj = SystemUserProfile.objects.get(id=request.GET.get('user_id'))

        user_data={'first_name':user_obj.first_name,'last_name':user_obj.last_name,
                   'city':user_obj.city.city,'role':user_obj.role.role,'email':user_obj.email,
                   'user_status':user_obj.status,'employee_id':user_obj.employee_id,
                   'contact_no':user_obj.contact_no,'address':user_obj.address
                   }
        data = {'success': 'true', 'user_data': user_data}
        print data
    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|get_system_user_details', e
        print 'Exception', e
        data = {'success': 'false', 'error': 'Exception ' + str(e)}
    return HttpResponse(json.dumps(data), content_type='application/json')


def head_admin(request):
    final_list=[]
    try:
        print 'views.py|head_admin'
        try:
            role_obj = UserRole.objects.get(role="H.O.Admin")
            head_admin_list = SystemUserProfile.objects.filter(role=role_obj)
            # get head admin data list
            for h in head_admin_list:
                head_admin_data ={'id':str(h.id),
                              'name':str(h.first_name)+' '+str(h.last_name),
                              'contact':str(h.contact_no),
                              'email':str(h.email),
                              'status':str(h.status),
                              'actions':'<a class="icon-pencil" title="Edit" onclick="edit_admin_modal('+ str(h.id) +');"></a>',
                              }
                final_list.append(head_admin_data)
            data = {'data':final_list}
        except Exception as e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|views.py|head_admin', e
            print 'Exception', e
            data = {'success': 'false', 'error': 'Exception ' + str(e)}
    except Exception, e:
        print 'Exception', e
    return HttpResponse(json.dumps(data), content_type='application/json')
