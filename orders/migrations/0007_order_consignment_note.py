# Generated by Django 4.0 on 2022-06-17 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_options_alter_order_status_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='consignment_note',
            field=models.CharField(default='', max_length=25, verbose_name='ТТН'),
        ),
    ]