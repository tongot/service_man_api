# Generated by Django 2.2.12 on 2020-05-25 06:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0016_business_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='business',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.CharField(default='Botswana', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='email_address',
            field=models.CharField(default='customer@customer.com', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(default='customer', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(default='customer', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(default='0000000', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='street_address',
            field=models.CharField(default='customer', max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='street_address2',
            field=models.CharField(default='customer', max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
