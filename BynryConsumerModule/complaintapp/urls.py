
from complaintapp import views
from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', views.complaint, name='Complaint'),
    url(r'^get-complaint-data/', views.get_complaint_data, name='get_complaint_data'),
    url(r'^get-complaint-details/', views.get_complaint_details, name='get_complaint_details'),
    url(r'^get-consumer-details/', views.get_consumer_details, name='get_consumer_details'),
]