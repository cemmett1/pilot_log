# Generated by Django 4.1.1 on 2022-10-02 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logbook", "0009_logentry_no_pic_no_xc"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="certificate",
            options={"ordering": ("name", "-valid_until")},
        ),
        migrations.AddField(
            model_name="logentry",
            name="night",
            field=models.BooleanField(default=False),
        ),
    ]
