from django.contrib import admin

from iTeam.events.models import Event

class EventAdmin(admin.ModelAdmin):
    # DETAIL fields for one publication
    fieldsets = [
        ('Informations',    {'fields': ['title', 'author', 'date']}),
        ('Texte',           {'fields': ['text']}),
    ]

    # fields for ALL publications
    list_display = ('title', 'author', 'date')

    list_filter = ['date', 'author']
    search_fields = ['title', 'text']

admin.site.register(Event, EventAdmin)
