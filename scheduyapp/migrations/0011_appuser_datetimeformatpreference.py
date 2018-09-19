# Generated by Django 2.0.7 on 2018-09-19 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduyapp', '0010_auto_20180918_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='datetimeFormatPreference',
            field=models.CharField(choices=[('Y-m-d H:i', 'Y-m-d H:i'), ('Y-m-d H:i a', 'Y-m-d H:i a'), ('Y/m/d H:i', 'Y/m/d H:i'), ('Y/m/d H:i a', 'Y/m/d H:i a'), ('m-d-Y H:i', 'm-d-Y H:i'), ('m-d-Y H:i a', 'm-d-Y H:i a'), ('m/d/Y H:i', 'm/d/Y H:i'), ('m/d/Y H:i a', 'm/d/Y H:i a'), ('d-m-Y H:i', 'd-m-Y H:i'), ('d-m-Y H:i a', 'd-m-Y H:i a'), ('d/m/Y H:i', 'd/m/Y H:i'), ('d/m/Y H:i a', 'd/m/Y H:i a')], default='Y-m-d H:i a', max_length=12, verbose_name='Datetime format'),
        ),
    ]
