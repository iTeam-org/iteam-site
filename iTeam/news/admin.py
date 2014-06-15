from django.contrib import admin

from iTeam.news.models import News

# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    # DETAIL fields for a news
    fieldsets = [
        ('Informations',    {'fields': ['title', 'subtitle', 'author', 'pub_date']}),
        ('Donnees',         {'fields': ['text']}),
    ]

    # fields for ALL news
    list_display = ('title', 'subtitle', 'author', 'pub_date')

    list_filter = ['pub_date', 'author']
    search_fields = ['title', 'subtitle', 'text']

admin.site.register(News, NewsAdmin)
