from django.contrib import admin

from iTeam.events.models import Event

class EventAdmin(admin.ModelAdmin):
    # DETAIL fields for one publication
    fieldsets = [
        ('Informations',    {'fields': ['title', 'author', 'place', 'date_start', 'type', 'is_draft', 'image']}),
        ('Texte',           {'fields': ['text']}),
    ]

    # fields for ALL publications
    list_display = ('title', 'author', 'date_start')

    list_filter = ['author', 'place', 'type', 'is_draft']
    search_fields = ['title', 'place', 'text']

admin.site.register(Event, EventAdmin)



