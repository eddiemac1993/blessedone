# Generated by Django 4.1.5 on 2023-02-14 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0012_remove_ordermodel_items_orderitem"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitem",
            name="price",
        ),
        migrations.RemoveField(
            model_name="ordermodel",
            name="quantity",
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="customer.menuitem"
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                to="customer.ordermodel",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
