# Generated by Django 2.0.1 on 2018-08-21 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0010_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('access_dashboard', '控制面板'), ('access_score_manage', '成绩管理'), ('access_schedule_manage', '课程管理'), ('access_assignment_manage', '作业管理')),
            },
        ),
    ]
