# Generated by Django 3.0.6 on 2020-05-24 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tsts', '0006_auto_20200524_2243'),
    ]

    operations = [
        migrations.RenameField(
            model_name='t_result',
            old_name='right_answer',
            new_name='right_answered',
        ),
    ]
