# Generated by Django 4.0.4 on 2023-01-26 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_time_table_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time_table',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
