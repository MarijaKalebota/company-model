# Generated by Django 3.1 on 2020-08-07 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company_model_manager", "0003_auto_20200807_0924"),
    ]

    operations = [
        migrations.AlterField(
            model_name="node", name="height", field=models.BigIntegerField(),
        ),
    ]
