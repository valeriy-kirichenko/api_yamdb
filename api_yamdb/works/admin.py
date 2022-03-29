from django.contrib import admin

from .models import Titles, Categories


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    actions_on_bottom = True
    list_editable = ('category',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'


admin.site.register(Titles, TitlesAdmin)
admin.site.register(Categories)
