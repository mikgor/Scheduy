# Generated by Django 2.0.7 on 2018-07-19 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0004_taskgroup_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskgroup',
            name='colour',
            field=models.CharField(default='whitesmoke', max_length=30),
        ),
    ]
