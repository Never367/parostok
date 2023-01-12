from django.contrib import admin

from .models import Profile, WishList


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'city', 'address', 'postal_code')
    search_fields = ('user',)
    list_filter = ('city',)


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'wish_list_count')

    @admin.display(description='Кількість продуктів')
    def wish_list_count(self, obj):
        return obj.product.count()
