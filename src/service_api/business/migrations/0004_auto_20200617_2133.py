# Generated by Django 2.2.12 on 2020-06-17 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_auto_20200617_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessdirectors',
            name='social_links',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
