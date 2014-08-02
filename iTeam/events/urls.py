
from django.conf.urls import patterns, url

from iTeam.events import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^view/(?P<event_id>\d+)/$', views.detail, name='detail'),
    url(r'^edit/(?P<event_id>\d+)/$', views.edit, name='edit'),
)
