# Generated by Django 2.0.7 on 2018-07-19 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0002_auto_20180719_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskgroup',
            name='tasks',
            field=models.ManyToManyField(to='todoapp.Task'),
        ),
    ]
