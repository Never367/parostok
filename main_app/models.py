from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from smart_selects.db_fields import ChainedForeignKey
from elasticsearch.exceptions import ConnectionError

from .documents import ProductDoc


class Category(models.Model):

    def image_folder(self, filename):
        filename = f'{self.slug}.{filename.split(".")[1]}'
        return f'{self.slug}/{filename}'

    name = models.CharField(max_length=255, verbose_name='Назва категорії')
    slug = models.SlugField(unique=True, verbose_name='Посилання')
    image = models.ImageField(upload_to=image_folder, verbose_name='Зображення')

    class Meta:
        verbose_name = 'категорію'
        verbose_name_plural = 'категорії'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class SubCategory(models.Model):

    category = models.ForeignKey(Category,
                                 verbose_name='Категорія',
                                 on_delete=models.CASCADE,
                                 related_name='subcategories')
    name = models.CharField(max_length=255, verbose_name='Назва підкатегорії')
    slug = models.SlugField(unique=True, verbose_name='Посилання')

    class Meta:
        verbose_name = 'підкатегорія'
        verbose_name_plural = 'підкатегорії'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subcategory_detail',
                       kwargs={'category_slug': self.category.slug,
                               'slug': self.slug})


class Product(models.Model):

    PRODUCT_STATUS_ACTUAL = '_actual'
    PRODUCT_STATUS_PRE_ORDER = '_pre_order'
    PRODUCT_STATUS_NOT_ACTUAL = 'not_actual'

    PRODUCTS_STATUS_CHOICES = (
        (PRODUCT_STATUS_ACTUAL, 'Актуальний'),
        (PRODUCT_STATUS_PRE_ORDER, 'Попереднє замовлення'),
        (PRODUCT_STATUS_NOT_ACTUAL, 'Не актуальний')
    )

    category = models.ForeignKey(Category,
                                 verbose_name='Категорія',
                                 on_delete=models.CASCADE,
                                 related_name='products')
    subcategory = ChainedForeignKey(
        SubCategory,
        verbose_name='Підкатегорія',
        chained_field='category',
        chained_model_field='category',
        show_all=False,
        auto_choose=True,
        on_delete=models.CASCADE,
        related_name='products',
    )
    name = models.CharField(max_length=255, verbose_name='Назва продукту')
    slug = models.SlugField(unique=True, verbose_name='Посилання')
    description = models.TextField(verbose_name='Опис', blank=True)
    status_product = models.CharField(
        max_length=100,
        verbose_name='В наявності',
        choices=PRODUCTS_STATUS_CHOICES,
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукти'
        ordering = ('status_product', 'name')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={
            'category_slug': self.category.slug,
            'subcategory_slug': self.subcategory.slug,
            'slug': self.slug
        })

    def indexing(self):
        doc = ProductDoc(
            meta={'id': self.id},
            name=self.name,
            id=self.id,
            status_product=self.status_product
        )
        try:
            doc.save(index='product')
        except ConnectionError as e:
            print(e)
        return doc.to_dict(include_meta=True)


class ProductPrice(models.Model):

    PRODUCT_AGE_1 = '1_year'
    PRODUCT_AGE_2 = '2_years'
    PRODUCT_AGE_3 = '3_years'
    PRODUCT_AGE_4 = '4_years'

    PRODUCT_CONTAINER_0 = '0,5_l'
    PRODUCT_CONTAINER_1 = '1_l'
    PRODUCT_CONTAINER_2 = '2_l'
    PRODUCT_CONTAINER_3 = '3_l'
    PRODUCT_CONTAINER_4 = '4_l'
    PRODUCT_CONTAINER_5 = '5_l'

    PRODUCT_AGE_CHOICES = (
        (PRODUCT_AGE_1, '1 рік'),
        (PRODUCT_AGE_2, '2 роки'),
        (PRODUCT_AGE_3, '3 роки'),
        (PRODUCT_AGE_4, '4 роки')
    )

    PRODUCT_CONTAINER_CHOICES = (
        (PRODUCT_CONTAINER_0, '0,5 л'),
        (PRODUCT_CONTAINER_1, '1 л'),
        (PRODUCT_CONTAINER_2, '2 л'),
        (PRODUCT_CONTAINER_3, '3 л'),
        (PRODUCT_CONTAINER_4, '4 л'),
        (PRODUCT_CONTAINER_5, '5 л')
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Продукт', related_name='prices')
    product_age = models.CharField(
        max_length=100,
        verbose_name='Вік рослини',
        choices=PRODUCT_AGE_CHOICES,
    )
    product_container = models.CharField(
        max_length=100,
        verbose_name='Розмір контейнеру',
        choices=PRODUCT_CONTAINER_CHOICES,
    )
    price = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='Ціна')

    class Meta:
        verbose_name = 'ціну продукту'
        verbose_name_plural = 'ціни продуктів'
        ordering = ('price',)
        unique_together = ('product', 'product_age', 'product_container')

    def __str__(self):
        return f'{self.price}'


class ProductImage(models.Model):

    def image_folder(self, filename):
        filename = f'{self.product.slug}.{filename.split(".")[1]}'
        return f'{self.product.slug}/{filename}'

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name='Продукт', related_name='images')
    image = models.ImageField(upload_to=image_folder,
                              verbose_name='зображення')

    class Meta:
        verbose_name = 'зображення продукту'
        verbose_name_plural = 'зображення продуктів'
        ordering = ('product',)

    @admin.display(description='')
    def image_tag(self):
        return mark_safe(f'<img src="/media/{self.image}" width="150" height="150" />')

    def __str__(self):
        return f'{self.image}'


class BannerPromotion(models.Model):

    def image_folder(self, filename):
        filename = f'{self.name}.{filename.split(".")[1]}'
        return f'Банери/{self.name}/{filename}'

    name = models.CharField(max_length=255, verbose_name='назва банеру')
    link = models.CharField(max_length=255, verbose_name='посилання для банеру')
    image = models.ImageField(upload_to=image_folder, verbose_name='зображення')
    image_mobile = models.ImageField(upload_to=image_folder,
                                     verbose_name='зображення для маленьких екранів')
    date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'банер для головної сторінки'
        verbose_name_plural = 'банери для головної сторінки'
        ordering = ('-date',)

    def __str__(self):
        return self.name
