# Generated by Django 4.1.7 on 2023-05-25 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_alter_archivequestion_option1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='name',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]