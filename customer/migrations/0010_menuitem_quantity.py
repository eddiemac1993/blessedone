# Generated by Django 4.1.5 on 2023-02-13 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0009_orderitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
