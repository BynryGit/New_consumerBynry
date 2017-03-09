# __author__='Swapnil Kadu'
from serviceapp import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.service_request, name='Service'),
    url(r'^get-service-data/', views.get_service_data, name='get-service-data'),
    url(r'^get-service-details/', views.get_service_details, name='get_service_details'),
    url(r'^get-consumer-details/', views.get_consumer_details, name='get_consumer_details'),
   ]