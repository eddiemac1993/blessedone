# Generated by Django 4.1.5 on 2023-01-31 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0002_ordermodel_items_alter_ordermodel_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordermodel",
            name="city",
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="email",
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="phone_number",
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="street",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]