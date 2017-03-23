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
from serviceapp import urls as service_urls
from consumerapp import consumer_urls
from nscapp import nsc_urls
from complaintapp import urls as complaint_urls
from vigilanceapp import urls as vigilance_urls
from django.views.generic import TemplateView
from django.conf.urls.static import static

urlpatterns = patterns('',       
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', 'views.dashboard',name='dashboard'),
    url(r'^login/', 'views.login',name='login'),
    url(r'^system-user/', 'views.system_user',name='system-user'),
    url(r'^save_system_user_details/', 'views.save_system_user_details',name='save_system_user_details'),
    url(r'^update_system_user_details/', 'views.update_system_user_details',name='update_system_user_details'),
    url(r'^get_system_user_details/', 'views.get_system_user_details',name='get_system_user_details'),
    url(r'^head_admin/', 'views.head_admin',name='head_admin'),
    url(r'^branch_admin/', 'views.branch_admin',name='branch_admin'),
    url(r'^head_supervisor/', 'views.head_supervisor',name='head_supervisor'),
    url(r'^branch_supervisor/', 'views.branch_supervisor',name='branch_supervisor'),
    url(r'^branch_agent/', 'views.branch_agent',name='branch_agent'),
    url(r'^administrator/', 'views.administrator',name='administrator'),
    url(r'^save-new-role/', 'views.save_new_role',name='save_new_role'),
    url(r'^get-role-list/', 'views.get_role_list',name='get_role_list'),    
    url(r'^get-role-details/', 'views.get_role_details',name='get_role_details'),
    url(r'^update-role-details/', 'views.update_role_details',name='update_role_details'),
    url(r'^get-branch/', 'views.get_branch',name='get_branch'),
    url(r'^serviceapp/', include(service_urls)),
    url(r'^paymentapp/', include(urls)),
    url(r'^consumerapp/', include(consumer_urls)),
    url(r'^complaintapp/', include(complaint_urls)),
    url(r'^vigilanceapp/', include(vigilance_urls)),
    url(r'^nscapp/', include(nsc_urls)),
) + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
