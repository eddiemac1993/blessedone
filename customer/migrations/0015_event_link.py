# Generated by Django 4.1.5 on 2023-05-30 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0014_remove_menuitem_delivery_time_menuitem_deliveredtime"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="link",
            field=models.URLField(
                default="https://blessedtouchs.pythonanywhere.com/ad-list/"
            ),
        ),
    ]
