__author__ = 'Swapnil Kadu'
from crmapp import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.home, name='login'),
]
