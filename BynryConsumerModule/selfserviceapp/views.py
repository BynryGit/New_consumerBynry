__auther__ = "Vikas Kumawat"
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from BynryConsumerModuleapp.models import Zone, BillCycle, RouteDetail, Branch
from consumerapp.models import ConsumerDetails
from django.contrib.sites.shortcuts import get_current_site
import datetime
from django.http import HttpResponse
import json
from django.shortcuts import render

def home_screen(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|home_screen'
        data = {
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|home_screen', exe
        data = {}
    return render(request, 'self_service/home_screen.html', data)

def register_new_user(request):
    """To view complaints page"""
    try:
        print 'selfserviceapp|views.py|register_new_user'
        data = {
        }
    except Exception as exe:
        print 'Exception|selfserviceapp|views.py|register_new_user', exe
        data = {}
    return render(request, 'self_service/register_new_user.html', data)    