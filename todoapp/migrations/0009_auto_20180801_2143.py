# Generated by Django 2.0.7 on 2018-08-01 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0008_auto_20180731_2314'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskgroup',
            old_name='colour',
            new_name='color',
        ),
    ]
