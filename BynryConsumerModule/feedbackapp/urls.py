
from feedbackapp import views
from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', views.feedback, name='feedback'),
]