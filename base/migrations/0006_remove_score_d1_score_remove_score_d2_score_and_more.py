# Generated by Django 4.0.4 on 2022-04-18 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_score_d1_score_score_d2_score_score_d3_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='d1_score',
        ),
        migrations.RemoveField(
            model_name='score',
            name='d2_score',
        ),
        migrations.RemoveField(
            model_name='score',
            name='d3_score',
        ),
    ]
