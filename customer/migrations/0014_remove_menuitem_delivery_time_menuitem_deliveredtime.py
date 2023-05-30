# Generated by Django 4.1.5 on 2023-05-29 06:21

import customer.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0013_alter_menuitem_delivery_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="menuitem",
            name="delivery_time",
        ),
        migrations.AddField(
            model_name="menuitem",
            name="DeliveredTime",
            field=models.TextField(default=customer.models.default_delivered_time),
        ),
    ]
