# Generated by Django 3.2.3 on 2021-05-24 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_cart_shipping_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=100)),
                ('payment_id', models.CharField(max_length=100)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
    ]