__author__ = 'Swapnil Kadu'
from crmapp import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.home, name='login'),
    url(r'^complaints/', views.complaints, name='complaints'),
    url(r'^get-consumer-complaints/', views.get_consumer_complaints, name='get_consumer_complaints'),
    url(r'^services/', views.services, name='services'),
    url(r'^vigilance/', views.vigilance, name='vigilance'),
]
