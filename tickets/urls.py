from django.conf.urls import url
from tickets.views import all_bugs, all_features, create_ticket, add_comment, show_comments, thumb_up

urlpatterns = [
    url(r'^bugs/', all_bugs, name='bugs'),
    url(r'^features/', all_features, name='features'),
    url(r'^new/$', create_ticket, name='create_ticket'),
    url(r'^(?P<pk>\d+)/(?P<uid>\d+)/$', add_comment, name='add_comment'),
    url(r'^comments/(?P<pk>\d+)/$', show_comments, name='show_comments'),
    url(r'^thumbup/(?P<pk>\d+)/$', thumb_up, name='thumb_up'),
]