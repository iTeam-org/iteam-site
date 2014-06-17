from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from iTeam.pages import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iTeam.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^news/', include('iTeam.news.urls', namespace="news")),
    url(r'^membres/', include('iTeam.member.urls', namespace="member")),
    url(r'^pages/', include('iTeam.pages.urls', namespace="pages")),
    
    url(r'^$', views.home),
)

