from django.conf.urls import url
from tickets.views import all_bugs, all_features, create_ticket

urlpatterns = [
    url(r'^bugs/', all_bugs, name='bugs'),
    url(r'^features/', all_features, name='features'),
    url(r'^new/$', create_ticket, name='create_ticket'),
]