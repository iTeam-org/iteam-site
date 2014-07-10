from django.contrib import admin

from iTeam.publications.models import Publication

# Register your models here.

class PublicationAdmin(admin.ModelAdmin):
    # DETAIL fields for one publication
    fieldsets = [
        ('Informations',    {'fields': ['title', 'subtitle', 'pub_date', 'author']}),
        ('Bonus',           {'fields': ['image', 'type']}),
        ('Text',            {'fields': ['text']}),
    ]

    # fields for ALL publications
    list_display = ('title', 'subtitle', 'author', 'pub_date', 'type')

    list_filter = ['pub_date', 'author', 'type']
    search_fields = ['title', 'subtitle', 'text']

    # add author name for the publication based on the current logged user
    def save_model(self, request, obj, form, change):
        # set user
        obj.author = request.user
        # call the admin model save.
        super(PublicationAdmin, self).save_model(request, obj, form, change)


admin.site.register(Publication, PublicationAdmin)
