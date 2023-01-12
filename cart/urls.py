from django.urls import path
from .views import cart_detail, cart_add, cart_remove, cart_recalculate


urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<str:product_id>/<str:product_age>/<str:product_container>/<str:product_price>',
         cart_add, name='cart_add'),
    path('remove/<str:product_id>/<str:product_age>/<str:product_container>',
         cart_remove, name='cart_remove'),
    path('recalculate/<str:product_id>/<str:product_age>/<str:product_container>/<str:quantity>',
         cart_recalculate, name='cart_recalculate')
]
