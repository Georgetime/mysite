# Generated by Django 2.0.1 on 2018-09-10 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0028_auto_20180909_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='extra_grade',
            field=models.IntegerField(default=0),
        ),
    ]
