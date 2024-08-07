# Generated by Django 4.0.4 on 2024-07-21 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_time_table_title_event_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about_me',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'invalid': 'Please provide a valid email address.', 'unique': 'A user with that email already exists.'}, max_length=255, unique=True),
        ),
    ]
