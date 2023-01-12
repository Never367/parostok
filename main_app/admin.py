from django.contrib import admin

from main_app.models import Category, SubCategory, ProductPrice, ProductImage, Product, BannerPromotion


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',), }
    list_display = ('name',)


@admin.register(SubCategory)
class SubcategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',), }
    list_display = ('name', 'category')


class ProductPriceInline(admin.TabularInline):

    model = ProductPrice
    extra = 0


class ProductImageInline(admin.TabularInline):

    model = ProductImage
    extra = 0
    readonly_fields = ('image_tag',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',), }
    list_display = ('name', 'status_product', 'prices_count',
                    'images_count', 'user_wish_list_count')
    search_fields = ('name',)
    list_filter = ('status_product',)
    list_editable = ('status_product',)
    inlines = (ProductPriceInline, ProductImageInline)

    @admin.display(description='кількість цін')
    def prices_count(self, obj):
        return obj.prices.count()

    @admin.display(description='кількість зображень')
    def images_count(self, obj):
        return obj.images.count()

    @admin.display(description='у списках побажань')
    def user_wish_list_count(self, obj):
        return obj.wish_list.count()


@admin.register(BannerPromotion)
class BannerPromotionAdmin(admin.ModelAdmin):
    list_display = ('name',)
