from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    search_fields = ('name',)
    ordering = ('-id',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    search_fields = ('name',)
    ordering = ('-id',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('name',)
    ordering = ('-year',)
    list_filter = ('year', 'category')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'text',
        'author',
        'score',
        'pub_date',
        'title_id',
    )
    search_fields = ('text', 'author')
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('text', 'author')
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'
