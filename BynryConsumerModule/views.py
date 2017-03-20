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
from BynryConsumerModuleapp.models import UserPrivilege,Zone,BillCycle,RouteDetail,Branch,SystemUserProfile,City,UserRole,Branch
import json
import traceback
from datetime import datetime
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
        print 'views.py|save_system_user_details'
        city_obj = City.objects.get(city=request.GET.get('city'))
        role_obj = UserRole.objects.get(role=request.GET.get('role'))
        user_obj = SystemUserProfile(
            username=request.GET.get('email'),
            password=request.GET.get('password'),
            contact_no=request.GET.get('contact_no'),
            address=request.GET.get('address'),
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

        user_data={'user_id':user_obj.id,'first_name':user_obj.first_name,'last_name':user_obj.last_name,
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


def update_system_user_details(request):
    try:
        print 'views.py|update_system_user_details'
        user_obj = SystemUserProfile.objects.get(id=request.GET.get('user_id'))

        city_obj = City.objects.get(city=request.GET.get('city'))
        role_obj = UserRole.objects.get(role=request.GET.get('role'))

        user_obj.username=request.GET.get('email')
        user_obj.password=request.GET.get('password')
        user_obj.contact_no=request.GET.get('contact_no')
        user_obj.address=request.GET.get('address')
        user_obj.first_name=request.GET.get('first_name')
        user_obj.last_name=request.GET.get('last_name')
        user_obj.city=city_obj
        user_obj.employee_id=request.GET.get('emp_id')
        user_obj.role=role_obj
        user_obj.email=request.GET.get('email')
        user_obj.status=request.GET.get('user_status')
        user_obj.save()

        if request.GET.get('branch'):
            branch_obj = Branch.objects.get(branch_name=request.GET.get('branch'))
            user_obj.branch = branch_obj
            user_obj.save()
        data={'success':'True'}

    except Exception, e:
        print 'exception ', str(traceback.print_exc())
        print 'Exception|views.py|update_system_user_details', e
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


def head_supervisor(request):
    final_list=[]
    try:
        print 'views.py|head_supervisor'
        try:
            role_obj = UserRole.objects.get(role="H.O.Supervisor")
            head_supervisor_list = SystemUserProfile.objects.filter(role=role_obj)
            # get head admin data list
            for h in head_supervisor_list:
                head_admin_data ={'id':str(h.id),
                              'name':str(h.first_name)+' '+str(h.last_name),
                              'contact':str(h.contact_no),
                              'email':str(h.email),
                              'status':str(h.status),
                              'actions':'<a class="icon-pencil" title="Edit" onclick="edit_supervisor_modal('+ str(h.id) +');"></a>',
                              }
                final_list.append(head_admin_data)
            data = {'data':final_list}
        except Exception as e:
            print 'exception ', str(traceback.print_exc())
            print 'Exception|views.py|head_supervisor', e
            print 'Exception', e
            data = {'success': 'false', 'error': 'Exception ' + str(e)}
    except Exception, e:
        print 'Exception', e
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
def save_new_role(request):
    try:
        print 'views.py|save_new_role'

        privilege_list = request.POST.get('privilege_list')
        privilege_list = privilege_list.split(',')

        new_role_obj = UserRole(
            role=request.POST.get('roll_name'),
            description=request.POST.get('description'),
            status="Active",
            #created_by=request.session['login_user'],
            #updated_by=request.session['login_user'],
            created_on=datetime.now(), 
            updated_on=datetime.now(),            

        );
        new_role_obj.save();

        for list_obj in privilege_list:
            obj = UserPrivilege.objects.get(privilege=list_obj) 
            new_role_obj.privilege.add(obj)
            new_role_obj.save()        

        data = {
            'success':  'true',
            'message': 'Consumer created successfully.'
        }
    except Exception, e:
        print 'Exception|views.py|save_new_role', e
        data = {
            'success': 'false',
            'message': str(e)
        }
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_role_list(request):
    try:
        print 'views.py|get_role_list'

        data = {}
        final_list = []
        try:
            role_obj_list = UserRole.objects.all()            

            for role_obj in role_obj_list:
                role = role_obj.role
                description = role_obj.description
                created_on = role_obj.created_on.strftime("%Y-%m-%d")
                associated_user = '--'

                if role_obj.status == 'Active':
                    status = '<span style="cursor: default;" class="btn btn-success">Active</span>'
                else:
                    status = '<span style="cursor: default;" class="btn btn-danger">Inactive</span>'

                action = '<a> <i class="fa fa-pencil" aria-hidden="true" onclick="edit_consumer(' + str(role_obj.id) + ')"></i> </a>'

                role_data = {
                    'role': role,
                    'description': description,
                    'created_on': created_on,
                    'associated_user': associated_user,
                    'status': status,
                    'action': action
                }
                final_list.append(role_data)
            data = {'success': 'true', 'data': final_list}
        except Exception as e:
            print 'Exception|views.py|get_role_list', e
            data = {'success': 'false', 'message': 'Error in  loading page. Please try after some time'}
    except MySQLdb.OperationalError, e:
        print 'Exception|views.py|get_role_list', e
    except Exception, e:
        print 'Exception|views.py|get_role_list', e
    return HttpResponse(json.dumps(data), content_type='application/json')
