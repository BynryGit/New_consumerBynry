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

class WebUserProfile(User):
	consumer_id = models.ForeignKey(ConsumerDetails, blank=False)

	status = models.CharField(max_length=20, default='Active', choices=ROLE_STATUS)
	created_by = models.CharField(max_length=500, blank=False, null=False)
	updated_by = models.CharField(max_length=500, blank=True, null=True)
	created_on = models.DateTimeField(default=django.utils.timezone.now)
	updated_on = models.DateTimeField(blank=True, null=True)
	is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

	def __unicode__(self):
		return unicode(str(self.username))