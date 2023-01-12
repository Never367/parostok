from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404

from account.models import Profile
from .models import Order, OrderItem
from cart.cart import Cart
from .tasks import order_created
from account.tasks import user_register

User = get_user_model()


def order_create(request):

    cart = Cart(request)
    if request.method == 'POST' and cart:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        city = request.POST.get('city')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code')
        comment = request.POST.get('comment')
        delivery_type = request.POST.get('delivery_type')
        payment_type = request.POST.get('payment_type')
        if request.user.is_authenticated:
            user = request.user
        else:
            # automatic user registration at checkout
            if not User.objects.filter(username=email):
                new_user = User.objects.create(
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    is_active=False
                )
                new_user.set_unusable_password()
                new_user.save()
                Profile.objects.create(
                    user=new_user,
                    phone_number=phone_number,
                    city=city,
                    address=address,
                    postal_code=postal_code
                )
                current_site = get_current_site(request)
                use_https = request.is_secure()
                user_register.delay(new_user.email, current_site.domain, use_https)
                user = new_user
            else:
                user = get_object_or_404(User, username=email)
        order = Order.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            city=city,
            address=address,
            postal_code=postal_code,
            comment=comment,
            delivery_type=delivery_type,
            payment_type=payment_type,
        )
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     product_age=item['product_age'].get_product_age_display(),
                                     product_container=item['product_container'].get_product_container_display(),
                                     price=item['price'],
                                     quantity=item['quantity']
                                     )
        # clearing the cart
        cart.clear()
        # start an asynchronous task
        order_created.delay(order.id)
        return render(request, 'created.html', {'order': order})
    else:
        return render(request, 'create.html', {'cart': cart})
