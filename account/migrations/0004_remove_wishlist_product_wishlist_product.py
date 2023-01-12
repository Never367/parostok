# Generated by Django 4.0 on 2022-06-19 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_productimage_image'),
        ('account', '0003_alter_profile_options_alter_wishlist_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='product',
            field=models.ManyToManyField(to='main_app.Product', verbose_name='Продукт'),
        ),
    ]