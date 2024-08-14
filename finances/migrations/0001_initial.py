# Generated by Django 4.1.5 on 2024-08-13 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Expense",
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
                ("date", models.DateField()),
                (
                    "company",
                    models.CharField(
                        choices=[("GEN", "General"), ("CMM", "CMM"), ("SC", "SC")],
                        max_length=3,
                    ),
                ),
                ("reason", models.TextField()),
                ("category", models.CharField(max_length=100)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
