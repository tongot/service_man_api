# Generated by Django 2.2.12 on 2020-06-16 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='articles_number',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='country',
            name='phone_number_structure',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
