# Generated by Django 4.1.5 on 2024-06-23 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0017_alter_ad_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menuitem",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="ordermodel",
            name="specifics",
            field=models.TextField(default="example@example.com"),
        ),
    ]
