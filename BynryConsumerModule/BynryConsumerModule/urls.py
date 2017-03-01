"""BynryConsumerModule URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.contrib import admin
from django.conf.urls import patterns, include, url
from BynryConsumerModule import settings
from paymentapp import urls

from django.views.generic import TemplateView
urlpatterns = patterns('',       
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', 'views.dashboard',name='dashboard'),
    url(r'^consumer-list/', 'views.consumer_list',name='consumer_list'),
    url(r'^consumer-details/', 'views.consumer_details',name='consumer_details'),            
    url(r'^complaints/', 'views.complaints',name='complaints'),
    url(r'^services/', 'views.services',name='services'),
    url(r'^vigilance-cases/', 'views.vigilance_cases',name='vigilance_cases'),
    url(r'^paymentapp/', include(urls)),
    #url(r'^payments/', 'views.payments',name='payments'),
    
)
