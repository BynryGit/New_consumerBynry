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
import dateutil.relativedelta

# importing mysqldb and system packages
import MySQLdb, sys
from django.db.models import Q
from django.db.models import F
from django.db import transaction
import pdb
import csv
import json
# importing exceptions
from django.db import IntegrityError
import operator
from django.db.models import Q
from datetime import date, timedelta
from django.views.decorators.cache import cache_control
# HTTP Response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import dateutil.relativedelta
from django.db.models import Count
from datetime import date
import calendar
import urllib2
import random
from .models import *

SERVER_URL = "http://52.66.133.35"


# SERVER_URL = "http://127.0.0.1:8000"


@csrf_exempt
def signin(request):
    data = {}
    try:
        if request.POST:
            print 'logs: login request with: ', request.POST
            username = request.POST['username']
            password = request.POST['password']
            try:
                user_obj = SystemUserProfile.objects.get(username=username)
                try:
                    user = authenticate(username=username, password=password)
                    if user:
                        if user.is_active:
                            user_profile_obj = SystemUserProfile.objects.get(username=username)
                            # request.session['user_role'] = user_profile_obj.user_role.role_name
                            try:
                                request.session['login_user'] = user_profile_obj.username
                                request.session['user_id'] = int(user_profile_obj.id)
                                request.session['branch_id'] = int(user_profile_obj.branch.id)
                                request.session[
                                    'first_name'] = user_profile_obj.user_first_name
                                login(request, user)
                            except Exception as e:
                                print e
                            data = {'success': 'true', 'username': request.session['first_name']}
                        else:
                            data = {'success': 'false', 'message': 'User Is Not Active'}
                            return HttpResponse(json.dumps(data), content_type='application/json')
                    else:
                        data = {'success': 'Invalid Password', 'message': 'Invalid Password'}
                        return HttpResponse(json.dumps(data), content_type='application/json')
                except:
                    data = {'success': 'Invalid Username', 'message': 'Invalid Username'}
                    return HttpResponse(json.dumps(data), content_type='application/json')
            except:
                data = {'success': 'Invalid Username', 'message': 'Invalid Username'}
                return HttpResponse(json.dumps(data), content_type='application/json')

    except MySQLdb.OperationalError, e:
        print e
        data = {'success': 'false', 'message': 'Internal server'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print 'Exception ', e
        data = {'success': 'false', 'message': 'Invalid Username or Password'}
    return HttpResponse(json.dumps(data), content_type='application/json')


def signing_out(request):
    logout(request)
    return render_to_response('login.html', dict(
        message_logout='You have successfully logged out.'
    ), context_instance=RequestContext(request))


@csrf_exempt
def forgot_password(request):
    # pdb.set_trace()
    username = request.POST.get("email")
    try:
        if request.POST:
            try:
                user_obj = SystemUserProfile.objects.get(username=username)
                print "user_obj", user_obj
                if user_obj:
                    print '.........username......', user_obj.username
                    print '.........user_id......', user_obj.user_id
                    ret = u''
                    ret = ''.join(random.choice('0123456789ABCDEF') for i in range(6))
                    OTP = ret
                    print "OTP", OTP
                    user_reset_password_mail(user_obj, OTP)
                    data = {'success': 'true', 'message': 'Login Successfully'}
                else:
                    data = {'success': 'true', 'message': 'Invalid Username'}


            except Exception as e:
                print e
                data = {'success': 'Invalid Username', 'message': 'Invalid Username'}
                print "INvalid", data

    except Exception as e:
        print e
        data = {'success': 'false', 'message': 'Invalid Username'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    except Exception, e:
        print 'Exception|view_py|forgot_pwd', e
    return HttpResponse(json.dumps(data), content_type='application/json')


def user_reset_password_mail(user_obj, OTP):
    poc = str(user_obj.usre_email_id)
    gmail_user = "donotreply@city-hoopla.com"  # "cityhoopla2016"
    gmail_pwd = "Hoopla123#"  # "cityhoopla@2016"
    FROM = 'Team CityHoopla<donotreply@city-hoopla.com>'
    TO = [poc]
    try:
        TEXT = "Dear " + str(
            user_obj.user_first_name) + ", \n\n" + "Greetings from CityHoopla !!! \n\n" + "Click on the link below to reset your password!!!" + "\n" + SERVER_URL + "/reset-password/?user_id=" + str(
            user_obj.user_id) + "\n\n" + "Best Wishes," + '\n' + "Team CityHoopla "
        SUBJECT = "Reset Password Link!"
        # server = smtplib.SMTP_SSL()
        # server = smtplib.SMTP("smtp.gmail.com", 587)
        server = smtplib.SMTP("smtpout.asia.secureserver.net", 80)
        # server = smtplib.SMTP_TSL('smtpout.secureserver.net', 465)
        server.ehlo()
        # server.starttls()
        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.quit()
    except SMTPException, e:
        print e
    return 1


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reset_password(request):
    user_id = request.GET.get('user_id')
    print user_id
    data = {'user_id': user_id}
    return render(request, 'Admin/reset_password.html', data)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reset_new_password(request):
    try:
        # pdb.set_trace()
        print 'in login'
        if request.POST:
            user_id = request.POST.get('user_id')
            try:
                print "user_id", user_id
                user_obj1 = SystemUserProfile.objects.get(user_id=user_id)
                username = user_obj1.usre_email_id

                user_obj = SystemUserProfile.objects.get(usre_email_id=username)
                new_password = request.POST.get('confirm_password')
                user_obj.set_password(request.POST.get('confirm_password'));
                user_obj.save();
                reset_password_mail(user_obj, new_password)

                data = {
                    'success': 'true',
                    'message': 'Password Updated Successfully.'
                }
                print "DATA", data

            except Exception, e:
                print 'Exception', e
                data = {
                    'success': 'false',
                    'message': 'Password Updated Successfully.'
                }


    except Exception, e:
        data = {
            'success': 'false',
            'message': str(e)
        }
    print data
    return HttpResponse(json.dumps(data), content_type='application/json')


def reset_password_mail(user_obj, OTP):
    poc = str(user_obj.usre_email_id)
    gmail_user = "donotreply@city-hoopla.com"  # "cityhoopla2016"
    gmail_pwd = "Hoopla123#"  # "cityhoopla@2016"
    FROM = 'Team CityHoopla<donotreply@city-hoopla.com>'
    TO = [poc]
    try:
        TEXT = "Dear " + str(
            user_obj.user_first_name) + ", \n\n" + "Greetings from CityHoopla !!! \n\n" + "Your password has been successfully chnaged. Please find below your login credentials to manage your Account. \n\n" + "Username: " + str(
            user_obj.usre_email_id) + "\n" + "Password: " + str(
            OTP) + '\n\n' + "Click on the link below to configure your account!!!" + "\n" + SERVER_URL + "/backoffice/" + "\n\n" + "Best Wishes," + '\n' + "Team CityHoopla "
        SUBJECT = "Your CityHoopla Password has been changed!"
        # server = smtplib.SMTP_SSL()
        # server = smtplib.SMTP("smtp.gmail.com", 587)
        server = smtplib.SMTP("smtpout.asia.secureserver.net", 80)
        # server = smtplib.SMTP_TSL('smtpout.secureserver.net', 465)
        server.ehlo()
        # server.starttls()
        server.login(gmail_user, gmail_pwd)
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        server.sendmail(FROM, TO, message)
        server.quit()
    except SMTPException, e:
        print e
    return 1
