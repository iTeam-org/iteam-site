from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from iTeam.pages import views

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'iTeam.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^publications/', include('iTeam.publications.urls', namespace="publications")),
    url(r'^membres/', include('iTeam.member.urls', namespace="member")),
    url(r'^pages/', include('iTeam.pages.urls', namespace="pages")),
    url(r'^events/', include('iTeam.events.urls', namespace="events")),

    url(r'^$', views.home),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
