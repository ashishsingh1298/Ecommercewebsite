# Generated by Django 3.0.5 on 2020-06-12 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_orders_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='contact_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
