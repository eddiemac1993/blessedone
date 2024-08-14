# Generated by Django 4.1.5 on 2024-08-14 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name="expense",
            name="company",
            field=models.CharField(
                choices=[("SC", "SC"), ("CMM", "CMM")], max_length=3
            ),
        ),
        migrations.AddField(
            model_name="expense",
            name="tags",
            field=models.ManyToManyField(blank=True, to="finances.tag"),
        ),
    ]
