from django.contrib.auth import get_user_model
from django.db import models
from main_app.models import Product, ProductPrice
from django.contrib import admin

User = get_user_model()


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Нове замовлення'),
        (STATUS_IN_PROGRESS, 'В обробці'),
        (STATUS_COMPLETED, 'Виконано'),
        (STATUS_CANCELED, 'Скасовано')
    )

    DELIVERY_TYPE_PICK_UP = 'pick_up'
    DELIVERY_TYPE_NOVA_P = 'delivery_nova_p'
    DELIVERY_TYPE_UKR_P = 'delivery_ukr_p'

    DELIVERY_TYPE_CHOICES = (
        (DELIVERY_TYPE_PICK_UP, 'Самовивіз'),
        (DELIVERY_TYPE_NOVA_P, 'Новою поштою'),
        (DELIVERY_TYPE_UKR_P, 'Укрпоштою'),
    )

    PAYMENT_TYPE_CASH = 'cash'
    PAYMENT_TYPE_CARD = 'card'

    PAYMENT_TYPE_CHOICES = (
        (PAYMENT_TYPE_CASH, 'Накладеним платежем'),
        (PAYMENT_TYPE_CARD, 'Оплата на карту')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Користувач', related_name='orders')
    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name='Прізвище')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефону')
    email = models.EmailField(verbose_name='Эл. пошта')
    city = models.CharField(max_length=100, verbose_name='Місто')
    address = models.CharField(max_length=250, verbose_name='Адреса')
    postal_code = models.CharField(max_length=20, verbose_name='Поштовий індекс')
    created = models.DateField(auto_now_add=True, verbose_name='Створено')
    updated = models.DateTimeField(auto_now=True, verbose_name='Оновлено')
    consignment_note = models.CharField(default='', max_length=25, verbose_name='ТТН')
    paid = models.BooleanField(default=False, verbose_name='Сплачено')
    comment = models.TextField(verbose_name='Коментар до замовлення', blank=True)
    delivery_type = models.CharField(
        max_length=100,
        verbose_name='Тип доставки',
        choices=DELIVERY_TYPE_CHOICES,
    )
    status_order = models.CharField(
        max_length=100,
        verbose_name='Статус замовлення',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    payment_type = models.CharField(
        max_length=100,
        verbose_name='Тип оплати',
        choices=PAYMENT_TYPE_CHOICES,
        default=PAYMENT_TYPE_CARD
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'замовлення'
        verbose_name_plural = 'замовлення'

    def __str__(self):
        return f'№ {self.id} від {self.created}'

    @admin.display(description='сума')
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Замовлення')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Продукт')
    product_age = models.CharField(max_length=100, verbose_name='Вік рослини')
    product_container = models.CharField(max_length=100, verbose_name='Розмір контейнеру')
    price = models.DecimalField(default=0, max_digits=10, decimal_places=0, verbose_name='Ціна')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')

    class Meta:
        verbose_name = 'Предмети замовлення'
        verbose_name_plural = 'Предмети замовлення'

    def __str__(self):
        return ''

    def get_cost(self):
        return self.price * self.quantity
