# Generated by Django 2.2.12 on 2020-05-08 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0011_auto_20200507_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_neg',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='product_available',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='product_new',
            field=models.BooleanField(default=1),
        ),
    ]
