# Generated by Django 4.1.7 on 2023-05-23 15:15

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_student_birth_day_student_image_student_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivequestion',
            name='option1',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='archivequestion',
            name='option2',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='archivequestion',
            name='option3',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='archivequestion',
            name='option4',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='archivequestion',
            name='question',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='option1',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='option2',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='option3',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='slide',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='video',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
