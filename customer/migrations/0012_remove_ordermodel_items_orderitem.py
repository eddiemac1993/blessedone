# Generated by Django 4.1.5 on 2023-02-14 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0011_remove_menuitem_quantity_ordermodel_quantity_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ordermodel",
            name="items",
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField(default=1)),
                ("price", models.DecimalField(decimal_places=2, max_digits=7)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="customer.menuitem",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="customer.ordermodel",
                    ),
                ),
            ],
        ),
    ]
