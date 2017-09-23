import django
from django.db import models
from BynryConsumerModuleapp.models import City, BillCycle, RouteDetail

from consumerapp.models import ConsumerDetails
from crmapp.models import ConsumerData


# Create your models here.

IS_DELETED = (
    (True, True),
    (False, False),
)
class ServiceRequestType(models.Model):
    request_type = models.CharField(max_length=100,blank=False, null=False)
    created_by = models.CharField(max_length=500, blank=False, null=False)
    updated_by = models.CharField(max_length=500, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.request_type)


class ServiceRequestSubType(models.Model):
    type = models.ForeignKey(ServiceRequestType,blank=False,name=False)
    sub_type = models.CharField(max_length=100,blank=False, null=False)
    created_by = models.CharField(max_length=500, blank=False, null=False)
    updated_by = models.CharField(max_length=500, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.sub_type)

class ServiceRequest(models.Model):
    SERVICE_STATUS = (
        ('Sent', 'Sent'),
        ('In Progress', 'In Progress'),
        ('Unresolved', 'Unresolved'),
        ('Resolved', 'Resolved'),
    )
    SERVICE_SOURCE = (
        ('Mobile', 'Mobile'),
        ('Web', 'Web'),
        ('CTI', 'CTI'),
    )
    service_no = models.CharField(max_length=50, blank=True, null=True)
    service_type = models.ForeignKey(ServiceRequestType, blank=False, null=True)
    subtype = models.ForeignKey(ServiceRequestSubType, blank=True, null=True)
    consumer_id = models.ForeignKey(ConsumerDetails, blank=False, null=True)
    consumer_data_id = models.ForeignKey(ConsumerData, blank=True, null=True)
    request_date = models.DateTimeField(blank=True, null=True)
    request_closer_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=500, default='Open', choices=SERVICE_STATUS)
    source = models.CharField(max_length=500, default='Open', choices=SERVICE_SOURCE)
    consumer_remark = models.CharField(max_length=500, blank=True, null=True)
    closure_remark = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.CharField(max_length=500, blank=False, null=False)
    updated_by = models.CharField(max_length=500, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.service_type)
