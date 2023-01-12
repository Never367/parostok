from django.conf import settings

from main_app.models import Product


class Cart(object):

    def __init__(self, request):
        """
        Initializing the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, product_age, product_container, product_price, quantity=1):
        """
        Add a product to the cart or update its quantity.
        """
        product_key = f'{product.id}/{product_age}/{product_container}'
        if product_key not in self.cart:
            self.cart[product_key] = {
                'quantity': 0,
                'price': str(product_price)
            }
        self.cart[product_key]['quantity'] = quantity
        self.save()

    def save(self):
        # Cart session update
        self.session[settings.CART_SESSION_ID] = self.cart
        # Mark a session as "modified" to make sure it's saved
        self.session.modified = True

    def remove(self, product, product_age, product_container):
        """
        Removing an item from the cart.
        """
        product_key = f'{product.id}/{product_age}/{product_container}'
        if product_key in self.cart:
            del self.cart[product_key]
            self.save()

    def __iter__(self):
        """
        Iterating through the items in the cart and getting the products from the database.
        """
        for key in self.cart.keys():
            product_key = key.split('/')
            # getting product objects and adding them to cart
            product = Product.objects.get(id=product_key[0])
            self.cart[key]['product'] = product
            self.cart[key]['product_age'] = product.prices.get(
                product_id=product_key[0],
                product_age=product_key[1],
                product_container=product_key[2]
            )
            self.cart[key]['product_container'] = product.prices.get(
                product_id=product_key[0],
                product_age=product_key[1],
                product_container=product_key[2]
            )

        for item in self.cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def __len__(self):
        """
        Counting all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculating the cost of items in the cart.
        """
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Delete cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def recalculate(self, product_id, product_age, product_container, quantity):
        product_key = f'{product_id}/{product_age}/{product_container}'
        self.cart[product_key]['quantity'] = int(quantity)
        self.save()
