from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from recipes.models import (Favorite, Ingredient, IngredientRecipeMap, Recipe,
                            Subscribe)


User = get_user_model()


class IngredientRecipeMapInline(admin.TabularInline):
    model = IngredientRecipeMap
    raw_id_fields = ('ingredient',)
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'units')
    ordering = ('name',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'author', 'tags', 'created', )
    list_filter = ('title', 'author__username', 'tags',)
    search_fields = ('title', 'author__username',)
    fields = (
        ('author', 'title', 'slug'),
        ('created', 'modified'),
        ('image', 'show_image'),
        ('tags', 'cooking_time', 'description'),
        'count_times_in_favorite'
    )
    inlines = (IngredientRecipeMapInline,)
    readonly_fields = ('show_image', 'count_times_in_favorite', 'created',
                       'modified')

    def show_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" height="150px" />')

    def count_times_in_favorite(self, obj):
        return obj.favorites.count()

    count_times_in_favorite.short_description = (
        'Times recipe add in favorites')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'chooser', 'recipe',)
    ordering = ('id',)
    search_fields = ('chooser', 'recipe',)


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscriber', 'author',)
    ordering = ('id',)
    search_fields = ('subscriber', 'author',)


class MyUserAdmin(UserAdmin):
    list_filter = ('username', 'email', 'is_staff', 'is_superuser',)


admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(User, MyUserAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
