from django.db import models
from django.conf import settings

from main_app.models import Product


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                verbose_name='Користувач', related_name='profile')
    phone_number = models.CharField(max_length=15,
                                    verbose_name='Номер телефону')
    city = models.CharField(max_length=100, verbose_name='Місто')
    address = models.CharField(max_length=250, verbose_name='Адреса')
    postal_code = models.CharField(max_length=20,
                                   verbose_name='Поштовий індекс')

    class Meta:
        verbose_name = 'додаткові дані користувачів'
        verbose_name_plural = 'додаткові дані користувачів'

    def __str__(self):
        return f'Профіль {self.user}'


class WishList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                verbose_name='Користувач', related_name='wish_list')
    product = models.ManyToManyField(Product, verbose_name='Продукт',
                                     related_name='wish_list', blank=True)

    class Meta:
        verbose_name = 'список бажань'
        verbose_name_plural = 'список бажань'

    def __str__(self):
        return f'Список бажань {self.user}'
