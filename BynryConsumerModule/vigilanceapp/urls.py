
from vigilanceapp import views
from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', views.vigilance, name='Complaint'),
    url(r'^get-vigilance-data/', views.get_vigilance_data, name='get_vigilance_data'),
    url(r'^get-vigilance-details/', views.get_vigilance_details, name='get_vigilance_details'),
]