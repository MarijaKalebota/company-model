# Generated by Django 3.1 on 2020-08-07 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company_model_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='root',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company_model_manager.node'),
        ),
    ]