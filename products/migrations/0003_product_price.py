# Generated by Django 5.1 on 2024-12-01 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.FloatField(default=50.0),
            preserve_default=False,
        ),
    ]