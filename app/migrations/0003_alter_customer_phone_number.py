# Generated by Django 3.2.3 on 2021-05-18 11:20

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_customer_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='0', max_length=128, region=None),
        ),
    ]