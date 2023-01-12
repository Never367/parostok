# Generated by Django 4.0 on 2022-08-09 20:07

from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_remove_subcategory_name_plural_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='image',
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, upload_to=main_app.models.Category.image_folder, verbose_name='зображення'),
        ),
    ]
