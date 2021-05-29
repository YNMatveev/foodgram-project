from django.contrib import admin


from shopping_list.models import Purchase


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shopping_list')
    ordering = ('user',)
    search_fields = ('user',)


admin.site.register(Purchase, PurchaseAdmin)
