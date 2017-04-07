import django
from django.db import models
from django.contrib.auth.models import User
from BynryConsumerModuleapp.models import City
from consumerapp.models import ConsumerDetails

# Create your models here.
ROLE_STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)
IS_REGISTERED = (
    (True, True),
    (False, False),
)


# class WebUserProfile(User):
#     consumer_id = models.ForeignKey(ConsumerDetails, blank=True, null=True)
#
#     status = models.CharField(max_length=20, default='Active', choices=ROLE_STATUS)
#     created_by = models.CharField(max_length=500, blank=False, null=False)
#     updated_by = models.CharField(max_length=500, blank=True, null=True)
#     created_on = models.DateTimeField(default=django.utils.timezone.now)
#     updated_on = models.DateTimeField(blank=True, null=True)
#     is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
#
#     def __unicode__(self):
#         return unicode(str(self.username))

class ConsumerData(models.Model):
    consumer_no = models.ForeignKey(ConsumerDetails, blank=True, null=True)
    name = models.CharField(max_length=200, blank=False, null=True)
    email_id = models.CharField(max_length=50, blank=True, null=True)
    contact_no = models.CharField(max_length=50, blank=True, null=True)
    city = models.ForeignKey(City, blank=False, null=True)
    is_registered = models.BooleanField(choices=IS_REGISTERED, default=False)
    created_by = models.CharField(max_length=500, blank=False, null=True)
    updated_by = models.CharField(max_length=500, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return unicode(str(self.name))
