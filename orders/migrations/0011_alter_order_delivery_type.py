# Generated by Django 4.0 on 2022-08-29 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_type',
            field=models.CharField(choices=[('pick_up', 'Самовивіз'), ('delivery_nova_p', 'Новою поштою'), ('delivery_ukr_p', 'Укрпоштою')], max_length=100, verbose_name='Тип доставки'),
        ),
    ]