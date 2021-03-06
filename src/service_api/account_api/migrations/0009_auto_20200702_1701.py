# Generated by Django 2.2.12 on 2020-07-02 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account_api', '0008_merge_20200625_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='UserConfirmed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation_number', models.IntegerField(max_length=6)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
