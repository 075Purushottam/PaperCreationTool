# Generated by Django 4.2.2 on 2023-07-19 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToolCore', '0005_paper'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='class_name',
            field=models.CharField(default='class_not_defined', max_length=100),
        ),
        migrations.AddField(
            model_name='paper',
            name='subject_name',
            field=models.CharField(default='subject_not_defined', max_length=100),
        ),
    ]
