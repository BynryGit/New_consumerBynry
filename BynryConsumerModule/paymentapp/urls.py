from paymentapp import views
from django.conf.urls import include, url

urlpatterns = [
    #url(r'^open-payment-list/',views.open_payment_list, name='open-payment-list'),
    url(r'^payments/',views.payments, name='payments'),
    url(r'^online_payments/',views.online_payments, name='online_payments'),
    url(r'^paytm_payments/',views.paytm_payments, name='paytm_payments'),
    #url(r'^list-payment-deatail/',views.list_payment_deatail),
    #url(r'^export-to-excel/',views.export_to_excel),
]
