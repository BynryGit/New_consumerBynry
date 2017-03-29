__author__ = 'Vikas Kumawat'
from selfserviceapp import views
from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^index/', views.home_screen, name='home_screen'),
    url(r'^register-new-user/', views.register_new_user, name='register_new_user'),
    url(r'^my-bills/', views.my_bills, name='my_bills'),
    url(r'^manage-accounts/', views.manage_accounts, name='manage_accounts'),
    url(r'^add-new-account/', views.add_new_account, name='add_new_account'),
    url(r'^complaints/', views.complaints, name='complaints'),
    url(r'^services/', views.services, name='services'),
    url(r'^contact-us/', views.contact_us, name='contact_us'),
    # url(r'^my-bills/', views.my_bills, name='my_bills'),
    url(r'^quick-pay/', views.quick_pay, name='quick_pay'),

]
