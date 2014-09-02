from django.conf.urls import patterns, url

from iTeam.medias import views

urlpatterns = patterns(
    '',
    url(r'^fb/$', views.fb, name='fb'),
    url(r'^fb_post/$', views.fb_post, name='fb_post'),
    url(r'^fb_get_token/$', views.fb_get_token, name='fb_get_token'),
)
