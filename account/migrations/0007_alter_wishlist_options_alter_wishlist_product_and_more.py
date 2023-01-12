# Generated by Django 4.0 on 2022-06-20 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main_app', '0005_alter_productimage_image'),
        ('account', '0006_alter_profile_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wishlist',
            options={'verbose_name': 'список бажань', 'verbose_name_plural': 'список бажань'},
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='product',
            field=models.ManyToManyField(blank=True, related_name='wish_list', to='main_app.Product', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wish_list', to='auth.user', verbose_name='Користувач'),
        ),
    ]
