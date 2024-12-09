# Generated by Django 5.1.1 on 2024-11-08 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_cart_delivery_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='delivery_location',
            field=models.CharField(choices=[('inside_dhaka', 'Inside Dhaka'), ('outside_dhaka', 'Outside Dhaka')], default='inside_dhaka', max_length=20),
        ),
    ]
