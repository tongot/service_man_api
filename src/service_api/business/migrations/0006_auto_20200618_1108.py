# Generated by Django 2.2.12 on 2020-06-18 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_auto_20200618_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessprofile',
            name='business',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='business.Business'),
        ),
    ]