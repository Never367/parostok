# Generated by Django 4.0 on 2022-06-19 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_productimage_image'),
        ('account', '0004_remove_wishlist_product_wishlist_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='product',
            field=models.ManyToManyField(related_name='wish_list', to='main_app.Product', verbose_name='Продукт'),
        ),
    ]
