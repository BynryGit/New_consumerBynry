from django.shortcuts import render

# Create your views here.
def new_connection_list(request):
    try:
        print 'nscapp|views.py|new_connection'
    except Exception, e:
        print 'Exception|nscapp|views.py|new_connection', e
    return render(request, 'nsc_template/new_connection_list.html')

def add_new_consumer(request):
    try:
        print 'nscapp|views.py|add_new_consumer'
    except Exception, e:
        print 'Exception|nscapp|views.py|add_new_consumer', e
    return render(request, 'nsc_template/add_new_consumer.html')

def review_consumer_form(request):
    try:
        print 'nscapp|views.py|review_consumer_form'
    except Exception, e:
        print 'Exception|nscapp|views.py|review_consumer_form', e
    return render(request, 'nsc_template/review_consumer_form.html')