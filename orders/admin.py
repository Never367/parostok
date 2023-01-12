from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):

    model = OrderItem
    extra = 0
    readonly_fields = ('order', 'product', 'product_age', 'product_container',
                       'price', 'quantity', 'item_total')

    @admin.display(description='сума')
    def item_total(self, obj):
        return obj.price * obj.quantity


class OrderAdmin(admin.ModelAdmin):

    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'status_order',
                    'paid', 'consignment_note', 'get_total_cost', 'email', 'city', 'address', 'postal_code', 'comment',
                    'delivery_type', 'payment_type', 'created', 'updated')
    list_filter = ('paid', 'status_order', 'created', 'updated')
    list_editable = ('status_order', 'paid', 'consignment_note')
    inlines = (OrderItemInline,)
    ordering = ('-status_order', '-created')
    readonly_fields = ('user',)


admin.site.register(Order, OrderAdmin)
