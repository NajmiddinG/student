# Generated by Django 4.1.7 on 2023-05-28 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_test_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='progress',
        ),
    ]