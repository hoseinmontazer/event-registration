# Generated by Django 4.0.4 on 2024-07-21 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_user_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='image',
            new_name='avatar',
        ),
    ]
