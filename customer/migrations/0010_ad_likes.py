# Generated by Django 4.1.5 on 2023-05-23 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0009_remove_comment_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="ad",
            name="likes",
            field=models.PositiveIntegerField(default=0),
        ),
    ]