# Generated by Django 2.0.1 on 2018-09-06 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0018_score_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='level',
            field=models.CharField(choices=[('Null', 0), ('A+', 9), ('A', 8), ('A-', 7), ('B+', 6), ('B', 5), ('B-', 4), ('C+', 3), ('C', 2), ('C-', 1)], max_length=2),
        ),
    ]