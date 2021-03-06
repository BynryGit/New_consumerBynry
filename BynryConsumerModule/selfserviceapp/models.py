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
IS_DELETED = (
    (True, True),
    (False, False),
)
PROFILE_IMAGE_PATH = 'profile_images/'

class WebUserProfile(User):
    consumer_id = models.ForeignKey(ConsumerDetails, blank=True, null=True)
    profile_image= models.ImageField(upload_to=PROFILE_IMAGE_PATH,default=None,null=True,blank=True)
    status      = models.CharField(max_length=20, default='Active', choices=ROLE_STATUS)
    created_by  = models.CharField(max_length=500, blank=False, null=False)
    updated_by  = models.CharField(max_length=500, blank=True, null=True)
    created_on  = models.DateTimeField(default=django.utils.timezone.now)
    updated_on  = models.DateTimeField(blank=True, null=True)
    is_deleted  = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.username))


class UserAccount(models.Model):
    parent_consumer_no = models.ForeignKey(WebUserProfile, blank=True, null=True)
    consumer_id = models.ForeignKey(ConsumerDetails, blank=True, null=True)
    consumer_no = models.CharField(max_length=500, blank=True, null=False)
    created_by = models.CharField(max_length=500, blank=False, null=False)
    updated_by = models.CharField(max_length=500, blank=True, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_on = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.consumer_no))