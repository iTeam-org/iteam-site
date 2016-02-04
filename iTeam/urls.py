from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.sitemaps import Sitemap
from django.contrib import admin
admin.autodiscover()

from iTeam.pages import views as pages_views
from iTeam.publications import views as publications_views
from iTeam.publications.models import Publication
from iTeam.events.models import Event

##########
# SiteMap
##########

class PublicationsSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.75

    def items(self):
        return Publication.objects.filter(is_draft=False)

    def lastmod(self, obj):
        return obj.pub_date

    def location(self, obj):
        return obj.get_absolute_url()


class EventsSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.75

    def items(self):
        return Event.objects.filter(is_draft=False)

    def location(self, obj):
        return obj.get_absolute_url()


sitemaps = {
    'publications': PublicationsSitemap,
    'evenements': EventsSitemap,
}


##########
# Url
##########

urlpatterns = patterns('',
    url(r'^a/', include(admin.site.urls)),

    url(r'^publications/', include('iTeam.publications.urls', namespace="publications")),
    url(r'^membres/', include('iTeam.member.urls', namespace="member")),
    url(r'^pages/', include('iTeam.pages.urls', namespace="pages")),
    url(r'^events/', include('iTeam.events.urls', namespace="events")),

    url(r'^$', pages_views.home),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns(
    'django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)
