from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group

from recipes.models import (Favorite, Ingredient, IngredientRecipeMap, Recipe,
                            Subscribe)


class IngredientRecipeMapInline(admin.TabularInline):
    model = IngredientRecipeMap
    raw_id_fields = ('ingredient',)
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'units')
    ordering = ('name',)
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'author', 'tag', )
    ordering = ('id',)
    list_filter = ('title', 'author__username', 'tag',)
    search_fields = ('title', 'author__username',)
    fields = (
        ('author', 'title', 'slug'),
        ('image', 'show_image'),
        ('tag', 'cooking_time', 'description'),
        'get_times_to_favorites',
    )
    inlines = (IngredientRecipeMapInline,)
    readonly_fields = ('get_times_to_favorites', 'show_image',)

    #  save_on_top = True

    def show_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="40%" />')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'chooser', 'recipe',)
    ordering = ('id',)
    search_fields = ('chooser', 'recipe',)


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscriber', 'author',)
    ordering = ('id',)
    search_fields = ('subscriber', 'author',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Subscribe, SubscribeAdmin)

admin.site.unregister(Group)
