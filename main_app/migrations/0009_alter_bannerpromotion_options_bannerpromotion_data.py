# Generated by Django 4.0 on 2022-08-04 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_bannerpromotion_remove_subcategory_image_mobile_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bannerpromotion',
            options={'ordering': ('-data',), 'verbose_name': 'банер для головної сторінки', 'verbose_name_plural': 'банери для головної сторінки'},
        ),
        migrations.AddField(
            model_name='bannerpromotion',
            name='data',
            field=models.DateField(auto_now=True),
        ),
    ]
