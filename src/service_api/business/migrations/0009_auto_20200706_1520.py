# Generated by Django 2.2.12 on 2020-07-06 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0008_auto_20200627_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='approved',
            field=models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('NEW', 'NEW')], default='NEW', max_length=3),
        ),
    ]