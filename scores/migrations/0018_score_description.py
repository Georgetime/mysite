# Generated by Django 2.0.1 on 2018-08-25 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0017_auto_20180822_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
