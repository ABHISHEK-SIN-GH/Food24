# Generated by Django 3.2.3 on 2021-05-22 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_grand_total_orderplaced_shipping_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='locality',
            field=models.CharField(default='', max_length=200),
        ),
    ]