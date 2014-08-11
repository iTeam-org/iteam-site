
from django.conf.urls import patterns, url

from iTeam.events import views

urlpatterns = patterns(
    '',
    url(r'^list/$', views.index_list, name='index_list'),
    url(r'^week/(?P<year>\d+)/(?P<month>\d+)/(?P<week_of_month>\d+)/$', views.index_week, name='index_week'),
    url(r'^month/(?P<year>\d+)/(?P<month>\d+)/$', views.index_month, name='index_month'),
    url(r'^create/$', views.create, name='create'),
    url(r'^view/(?P<event_id>\d+)/$', views.detail, name='detail'),
    url(r'^edit/(?P<event_id>\d+)/$', views.edit, name='edit'),
)
