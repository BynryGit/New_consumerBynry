__author__ = 'Vikas Kumawat'
from selfserviceapp import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^index/', views.home_screen, name='home_screen'),
    url(r'^register-new-user/', views.register_new_user, name='register_new_user'),
]
