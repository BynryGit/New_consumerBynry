from django.db import models
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
#from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib import auth

#from constants import AppUserConstants, ExceptionLabel
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

# importing mysqldb and system packages
import MySQLdb, sys
from django.db.models import Q
from django.db.models import F
from django.db import transaction

import csv
import json
#importing exceptions
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError

from datetime import datetime
import uuid
from django.db.models.signals import class_prepared
import django
# Create your models here.


class User(User):
    user_id                        =       models.AutoField(primary_key=True, editable=False)
    user_name                      =       models.CharField(max_length=100,default=None,blank=True,null=True)

    def __unicode__(self):
        return unicode(self.operator_id)

