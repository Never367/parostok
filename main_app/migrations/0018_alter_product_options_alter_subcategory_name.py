# Generated by Django 4.0 on 2022-08-12 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('status_product', 'name'), 'verbose_name': 'продукт', 'verbose_name_plural': 'продукти'},
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Назва підкатегорії'),
        ),
    ]
