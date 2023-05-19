# Generated by Django 4.1.5 on 2023-05-19 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0006_remove_ad_image_adimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="ad",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("agriculture", "Agriculture"),
                    ("hardware", "Hardware"),
                    ("food", "Food"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="ad",
            name="price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="menuitem",
            name="category",
            field=models.ManyToManyField(related_name="items", to="customer.category"),
        ),
        migrations.AlterField(
            model_name="ordermodel",
            name="email",
            field=models.EmailField(default="example@example.com", max_length=254),
        ),
        migrations.AlterField(
            model_name="ordermodel",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to="customer.location",
            ),
        ),
        migrations.AlterField(
            model_name="ordermodel",
            name="specifics",
            field=models.EmailField(default="example@example.com", max_length=254),
        ),
    ]
