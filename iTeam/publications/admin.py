from django.contrib import admin

from iTeam.publications.models import Publication

# Register your models here.

class PublicationAdmin(admin.ModelAdmin):
    # DETAIL fields for one publication
    fieldsets = [
        ('Informations',    {'fields': ['title', 'subtitle', 'pub_date', 'author']}),
        ('Options',         {'fields': ['image', 'type', 'is_draft']}),
        ('Texte',           {'fields': ['text']}),
    ]

    # fields for ALL publications
    list_display = ('title', 'subtitle', 'author', 'pub_date', 'type', 'is_draft')

    list_filter = ['pub_date', 'author', 'type', 'is_draft']
    search_fields = ['title', 'subtitle', 'text']

admin.site.register(Publication, PublicationAdmin)
