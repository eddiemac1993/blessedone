# Generated by Django 4.1.5 on 2023-02-16 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0014_remove_ordermodel_price_ordermodel_order_items_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ordermodel",
            name="order_items",
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="items",
            field=models.ManyToManyField(
                blank=True, related_name="order", to="customer.menuitem"
            ),
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=0.0, max_digits=7, null=True
            ),
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="specifics",
            field=models.EmailField(default="example@email.com", max_length=254),
        ),
        migrations.DeleteModel(
            name="OrderItem",
        ),
    ]