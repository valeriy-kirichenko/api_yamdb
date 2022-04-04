from django.contrib import admin

from .models import Genres, Titles, Categories, Reviews, Comments


@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'year', 'description')
    actions_on_bottom = True
    list_editable = ('category',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    actions_on_bottom = True
    search_fields = ('name',)


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    actions_on_bottom = True
    search_fields = ('name',)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date', 'score')
    actions_on_bottom = True
    search_fields = ('text',)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date')
    actions_on_bottom = True
    search_fields = ('text',)
