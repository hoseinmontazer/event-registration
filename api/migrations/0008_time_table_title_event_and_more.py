# Generated by Django 4.0.4 on 2024-07-13 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_time_table_end_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='time_table',
            name='title_event',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='time_table',
            name='summery_event',
            field=models.CharField(max_length=2000),
        ),
    ]
