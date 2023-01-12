from main_app.models import Category
from cart.cart import Cart
from account.forms import LoginForm


def categories(request):
    categories_dict = {}
    for category in Category.objects.all():
        for subcategory in category.subcategories.all():
            if subcategory.products.exclude(status_product='not_actual'):
                if category in categories_dict:
                    categories_dict[category] += [subcategory]
                else:
                    categories_dict[category] = [subcategory]
    return {'categories_dict': categories_dict}


def cart(request):
    cart = Cart(request)
    return {'cart': cart}


def login_form(request):
    form = LoginForm()
    return {'login_form': form}
