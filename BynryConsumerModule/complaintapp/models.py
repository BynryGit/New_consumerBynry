from django.db import models
import django
from django.db import models
from django.utils import timezone
from consumerapp.models import ConsumerDetails

CONSUMER_DOCS_PATH ='images/consumer_docs_file/'
# Create your models here.

IS_DELETED = (
    (True, True),
    (False, False),
)

IMAGES_PATH = 'complaints/'

class ComplaintType (models.Model):
    complaint_type = models.CharField(max_length=500,blank = True, null = True)
    complaint_code = models.CharField(max_length=100,blank = True, null = True)
    updated_by = models.CharField(max_length=50 ,blank = True, null = True)
    created_on = models.DateTimeField(default = django.utils.timezone.now)
    updated_on = models.DateField(blank = True, null = True)
    created_by = models.CharField(max_length = 50)
    is_deleted = models.BooleanField(choices = IS_DELETED, default = False)

    def __unicode__(self):
        return unicode(self.complaint_type)


class ComplaintDetail(models.Model):

    COMPLAINT_STATUS = (
        ('WIP', 'WIP'),
        ('Closed', 'Closed'),
        ('Open', 'Open'),
    )

    COMPLAINT_SOURCE = (
        ('Mobile', 'Mobile'),
        ('Web', 'Web'),
        ('CTI', 'CTI'),
    )

    complaint_no = models.CharField(max_length=200, blank=False, null=True)
    complaint_type_id = models.ForeignKey(ComplaintType, blank = False, null = True)
    consumer_id = models.ForeignKey(ConsumerDetails, blank = False, null = True)
    remark = models.CharField(max_length = 200,blank = True, null = True)
    complaint_img=models.ImageField(upload_to=IMAGES_PATH,null=True,blank=True)
    complaint_status = models.CharField(max_length = 50, choices = COMPLAINT_STATUS)
    complaint_source = models.CharField(max_length = 50, choices = COMPLAINT_SOURCE)
    complaint_date = models.DateTimeField(blank = True,null = True)
    resolve_date = models.DateField(blank = True,null = True)
    closure_remark = models.CharField(max_length = 500,blank = True, null = True)
    created_on = models.DateTimeField(default = django.utils.timezone.now)
    updated_on = models.DateTimeField(blank = True, null = True)
    updated_by = models.CharField(max_length = 50,blank = True,null = True)
    created_by = models.CharField(max_length = 50)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.complaint_no)


class ComplaintImages(models.Model):
    consumer_id		= models.ForeignKey(ConsumerDetails,blank=True,null=True)
    document_files 	= models.FileField(upload_to=CONSUMER_DOCS_PATH, max_length=500, null=True, blank=True)
    creation_date 	= models.DateTimeField(null=True,blank=True)
    created_by 		= models.CharField(max_length=500,null=True,blank=True)
    updated_by 		= models.CharField(max_length=500,null=True,blank= True)
    updation_date	= models.DateTimeField(null=True,blank=True)

    def __unicode__(self):
        return unicode(self.id)