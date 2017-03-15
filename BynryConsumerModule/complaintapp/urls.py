
from complaintapp import views
from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', views.complaint, name='Complaint'),
    url(r'^get-complaint-data/', views.get_complaint_data, name='get_complaint_data'),
    url(r'^get-complaint-details/', views.get_complaint_details, name='get_complaint_details'),
    url(r'^get-consumer-details/', views.get_consumer_details, name='get_consumer_details'),
    url(r'^get-zone/', views.get_zone, name='get_zone'),
    url(r'^get-bill-cycle/', views.get_bill_cycle, name='get_bill_cycle'),
    url(r'^get-route/', views.get_route, name='get_route'),
]