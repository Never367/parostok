from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main_app.models import Product

from .cart import Cart

@require_POST
def cart_add(request, product_id, product_age, product_container, product_price):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product,
             product_age=product_age,
             product_container=product_container,
             product_price=product_price,
             quantity=1),
    return redirect('cart_detail')


def cart_remove(request, product_id, product_age, product_container):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product, product_age, product_container)
    return redirect('cart_detail')


@require_POST
def cart_recalculate(request, product_id, product_age, product_container, quantity):
    cart = Cart(request)
    cart.recalculate(
        product_id=product_id,
        product_age=product_age,
        product_container=product_container,
        quantity=quantity
    )
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})
