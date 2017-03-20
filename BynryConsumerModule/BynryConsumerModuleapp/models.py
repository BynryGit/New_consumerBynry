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



IS_DELETED = (
    (True, True),
    (False, False),
)

ROLE_STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)
class State(models.Model):
    state = models.CharField(max_length=500, blank=True)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.state)

class City(models.Model):
    city = models.CharField(max_length=500, default=None)
    state = models.ForeignKey(State, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.city)

class Pincode(models.Model):
    pincode = models.CharField(max_length=500, default=None)
    city = models.ForeignKey(City, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.pincode)


class Utility(models.Model):
    utility = models.CharField(max_length=100, blank=False, null=False)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.utility)

class Branch(models.Model):
    branch_name = models.CharField(max_length=250, blank=False, null=False)
    city = models.ForeignKey(City, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.branch_name)

class Zone(models.Model):
    zone_name = models.CharField(max_length=250, blank=False, null=False)
    branch = models.ForeignKey('Branch', blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.zone_name)

class BillCycle(models.Model):
    bill_cycle_code = models.CharField(max_length=100, blank=False, null=False)
    zone = models.ForeignKey('Zone', blank=True, null=True)
    area = models.ForeignKey('Area', blank=True, null=True)
    bill_cycle_name = models.CharField(max_length=100, blank=False, null=True)
    city = models.ForeignKey('City', blank=True, null=True)
    utility = models.ForeignKey('Utility', blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.bill_cycle_code)


class Area(models.Model):
    area_name = models.CharField(max_length=250, blank=False, null=False)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.area_name)

class RouteDetail(models.Model):
    route_code = models.CharField(max_length=500, blank=False, null=False)
    billcycle = models.ForeignKey(BillCycle, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.route_code)


class UserPrivilege(models.Model):
    privilege = models.CharField(max_length=500, blank=False, null=False)
    parent = models.ForeignKey('self', blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.privilege)


class UserRole(models.Model):
    role = models.CharField(max_length=500, blank=False, null=False)
    description = models.CharField(max_length=500, blank=True, null=True)
    privilege = models.ManyToManyField(UserPrivilege)
    status = models.CharField(max_length=20, default='Active', choices=ROLE_STATUS)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.role)

class SystemUserProfile(User):
    contact_no = models.CharField(max_length=15, blank=False, null=False)
    address = models.CharField(max_length=500, blank=True, null=False)
    user_first_name = models.CharField(max_length=500, blank=True, null=False)
    user_last_name = models.CharField(max_length=500, blank=True, null=False)
    address = models.CharField(max_length=500, blank=True, null=False)
    user_email = models.CharField(max_length=500, blank=True, null=False)
    city = models.ForeignKey(City, blank=False, null=True)
    role = models.ForeignKey(UserRole, blank=True, null=True)
    branch = models.ForeignKey(Branch, blank=True, null=True)
    employee_id = models.CharField(max_length=100, blank=True, null=False)
    status = models.CharField(max_length=20, default='Active', choices=ROLE_STATUS)
    created_by = models.CharField(max_length=500, blank=False, null=False)
    updated_by = models.CharField(max_length=500, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.username))


class BillingUnit(models.Model):
    B_U = models.CharField(max_length=20,blank=False,null=True)
    city = models.ForeignKey('City', blank=True, null=True)

    def __unicode__(self):
        return  unicode(str(self.B_U))

class ProcessingCycle(models.Model):
    P_C = models.CharField(max_length=20, blank=False, null=True)
    B_U = models.ForeignKey('BillingUnit', blank=False, null=True)

    def __unicode__(self):
        return  unicode(str(self.P_C))
