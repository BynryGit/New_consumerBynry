__author__ = 'Swapnil Kadu'
from crmapp import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.home, name='login'),
    url(r'^complaints/', views.complaints, name='complaints'),
    url(r'^get-consumer-complaints/', views.get_consumer_complaints, name='get_consumer_complaints'),
    url(r'^get-complaint-details/', views.get_complaint_details, name='get_complaint_details'),
    url(r'^save-complaint-details/', views.save_complaint_details, name='save_complaint_details'),
    url(r'^services/', views.services, name='services'),
]
