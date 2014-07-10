from django.conf.urls import patterns, url

from iTeam.publications import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^view/(?P<publication_id>\d+)/$', views.detail, name='detail'),
    url(r'^edit/(?P<publication_id>\d+)/$', views.edit, name='edit'),
)
