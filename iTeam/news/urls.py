from django.conf.urls import patterns, url

from iTeam.news import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^view/(?P<news_id>\d+)/$', views.detail, name='detail'),
)
