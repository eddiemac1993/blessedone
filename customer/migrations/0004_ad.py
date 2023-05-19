# Generated by Django 4.1.5 on 2023-05-17 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0003_menuitem_is_verified"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ad",
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
                ("image", models.ImageField(upload_to="ads/")),
                ("title", models.CharField(max_length=100)),
                ("phone_number", models.CharField(max_length=20)),
                ("description", models.TextField(blank=True)),
                (
                    "location",
                    models.CharField(default="Livingstone, Zambia", max_length=100),
                ),
            ],
        ),
    ]