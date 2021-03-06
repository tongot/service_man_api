# Generated by Django 2.2.12 on 2020-06-17 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_auto_20200616_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesscontactperson',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_person', to='business.Business'),
        ),
        migrations.AlterField(
            model_name='businessdirectors',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='directors', to='business.Business'),
        ),
    ]
