# Generated by Django 4.0.2 on 2022-02-06 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logbook", "0007_logentry_cross_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="logentry",
            name="slots",
            field=models.PositiveSmallIntegerField(default=1, help_text="Number of logbook slots for this entry."),
        ),
    ]
