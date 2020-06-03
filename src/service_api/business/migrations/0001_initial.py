# Generated by Django 2.2.12 on 2020-04-24 03:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('contact_persona_name', models.CharField(max_length=255)),
                ('contact_persona_phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('quantity', models.IntegerField()),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Business')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Business')),
            ],
        ),
        migrations.CreateModel(
            name='ProductReviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=5000)),
                ('stars', models.IntegerField(choices=[('GOOD', 1), ('BETTER', 2), ('COOL', 3), ('BEST', 4), ('EXCELLENT', 5)])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCommentReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=5000)),
                ('product_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.ProductReviews')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.ProductCategory'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('date_of_order', models.DateTimeField(auto_now_add=True)),
                ('approved', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], default='NO', max_length=3)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='business.Product')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessReviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=5000)),
                ('stars', models.IntegerField(choices=[('GOOD', 1), ('BETTER', 2), ('COOL', 3), ('BEST', 4), ('EXCELLENT', 5)])),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Business')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessCommentReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=5000)),
                ('business_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.BusinessReviews')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='business',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Location'),
        ),
        migrations.AddField(
            model_name='business',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='business',
            name='type_of_business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.BusinessType'),
        ),
    ]
