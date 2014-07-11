from django.conf.urls import patterns, url

from iTeam.medias import views

urlpatterns = patterns(
    '',
    url(r'^fb/$', views.fb, name='fb'),
)
