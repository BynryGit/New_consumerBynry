from django.db import models
import django
from django.db import models
from django.utils import timezone
from consumerapp.models import ConsumerDetails
from BynryConsumerModuleapp.models import *

# Create your models here.

IS_DELETED = (
    (True, True),
    (False, False),
)

class VigilanceType (models.Model):
    vigilance_type = models.CharField(max_length=500,blank = True, null = True)
    vigilance_code = models.CharField(max_length=100,blank = True, null = True)
    updated_by = models.CharField(max_length=50 ,blank = True, null = True)
    created_on = models.DateTimeField(default = django.utils.timezone.now)
    updated_on = models.DateField(blank = True, null = True)
    created_by = models.CharField(max_length = 50)
    is_deleted = models.BooleanField(choices = IS_DELETED, default = False)

    def __unicode__(self):
        return unicode(self.vigilance_type)


class VigilanceDetail(models.Model):

    VIGILANCE_STATUS = (
        ('WIP', 'WIP'),
        ('Closed', 'Closed'),
        ('Open', 'Open'),
    )

    VIGILANCE_SOURCE = (
        ('Mobile', 'Mobile'),
        ('Web', 'Web'),
        ('CTI', 'CTI'),
    )

    THEFT_FOUND = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    case_id = models.CharField(max_length=200, blank=False, null=True)
    vigilance_type_id = models.ForeignKey(VigilanceType, blank = False, null = True)
    consumer_id = models.ForeignKey(ConsumerDetails, blank = False, null = True)
    vigilance_remark = models.CharField(max_length = 200,blank = True, null = True)
    vigilance_status = models.CharField(max_length = 50, choices = VIGILANCE_STATUS)
    vigilance_source = models.CharField(max_length = 50, choices = VIGILANCE_SOURCE)
    registered_date = models.DateTimeField(blank = True,null = True)
    zone = models.ForeignKey(Zone, blank=False, null=True)
    bill_cycle = models.ForeignKey(BillCycle, blank=True, null=True)
    route = models.ForeignKey(RouteDetail, blank=True, null=True)
    theft_found = models.CharField(max_length=50, choices=THEFT_FOUND)
    created_on = models.DateTimeField(default = django.utils.timezone.now)
    updated_on = models.DateTimeField(blank = True, null = True)
    updated_by = models.CharField(max_length = 50,blank = True,null = True)
    created_by = models.CharField(max_length = 50)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.case_id)


class VigilancePenalyDetail(models.Model):
    PAYMENT_STATUS = (
        ('Closed', 'Closed'),
        ('Open', 'Open'),
    )

    PAYMENT_METHOD = (
        ('Online', 'Online'),
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
    )

    vigilance_id = models.ForeignKey(VigilanceDetail, blank=False, null=True)
    payment = models.CharField(max_length=200, blank=True, null=True)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.id)

class CourtCaseDetail(models.Model):
    CASE_STATUS = (
        ('Closed', 'Closed'),
        ('Open', 'Open'),
        ('Pending', 'Pending'),
    )

    vigilance_id = models.ForeignKey(VigilanceDetail, blank=False, null=True)
    court_remark = models.CharField(max_length=200, blank=True, null=True)
    case_status = models.CharField(max_length=50, choices=CASE_STATUS)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.id)