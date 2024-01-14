# Generated by Django 4.1.7 on 2024-01-14 09:01

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import student.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', ckeditor.fields.RichTextField(verbose_name='Savol')),
                ('option1', ckeditor.fields.RichTextField()),
                ('option2', ckeditor.fields.RichTextField()),
                ('option3', ckeditor.fields.RichTextField()),
                ('option4', ckeditor.fields.RichTextField()),
                ('correct', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name="To'g'ri javob")),
                ('choosen', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name="O'quvchi tanlagan javob")),
            ],
            options={
                'verbose_name': 'Testda tushgan savollar',
                'verbose_name_plural': 'Testda tushgan savollar',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Guruh nomi')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Guruh nomi',
                'verbose_name_plural': 'Guruhlar',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', ckeditor.fields.RichTextField(verbose_name='Savol')),
                ('answer', ckeditor.fields.RichTextField(verbose_name="To'gri javob")),
                ('option1', ckeditor.fields.RichTextField()),
                ('option2', ckeditor.fields.RichTextField()),
                ('option3', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Savollar',
                'verbose_name_plural': 'Savollar',
            },
        ),
        migrations.CreateModel(
            name='Science',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Fan',
                'verbose_name_plural': 'Fanlar',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Video nomi')),
                ('image', models.ImageField(upload_to='Video/', verbose_name='Video uchun rasm')),
                ('link', models.URLField(default='https://youtube.com', verbose_name='Video linki')),
                ('text', ckeditor.fields.RichTextField(verbose_name='Video uchun post yozing')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('group', models.ManyToManyField(to='student.group', verbose_name='Qaysi guruhlarga tegishli')),
                ('science', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.science', verbose_name='Qaysi fanga tegishli')),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videolar',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Test nomi')),
                ('number', models.IntegerField(default=10, verbose_name='Nechta savol ishlash kerak')),
                ('start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Qachon boshlanadi')),
                ('end', models.DateTimeField(default=student.models.five_day, verbose_name='Qachon tugaydi')),
                ('duration', models.TimeField(verbose_name='Qancha vaqt davom etadi')),
                ('required', models.BooleanField(default=False, verbose_name='Majburiymi')),
                ('possibilities', models.IntegerField(default=1, verbose_name='Imkoniyatlar soni')),
                ('answers', models.IntegerField(default=0, verbose_name="Minimal nechta savolni ishlash to'g'ri topishi")),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(to='student.group', verbose_name='Qaysi guruhlar uchun')),
                ('questions', models.ManyToManyField(to='student.question', verbose_name='Savollar')),
                ('science', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.science', verbose_name='Qaysi fandan')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='User/', verbose_name='Rasm')),
                ('location', models.CharField(blank=True, max_length=255, null=True, verbose_name='Manzil')),
                ('birth_day', models.DateField(blank=True, null=True, verbose_name="Tug'ilgan kun")),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Tel')),
                ('pagination', models.IntegerField(default=10)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.group', verbose_name='Guruhi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': "O'quvchi",
                'verbose_name_plural': "O'quvchilar",
            },
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Slide nomi')),
                ('image', models.ImageField(upload_to='Slides/', verbose_name='Rasm')),
                ('text', ckeditor.fields.RichTextField(verbose_name='Slide uchun matn')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('group', models.ManyToManyField(to='student.group', verbose_name='Qaysi guruhlar uchun')),
                ('science', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.science', verbose_name='Qaysi fanga doir')),
            ],
            options={
                'verbose_name': 'Slide',
                'verbose_name_plural': 'Slidelar',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(blank=True, max_length=100, null=True, verbose_name='Natija')),
                ('status', models.BooleanField(default=True, verbose_name="Holati(Tesdan o'tdi/o'tmadi)")),
                ('duration', models.TimeField(verbose_name='Qancha vaqt davom etgani')),
                ('finished', models.BooleanField(default=False, verbose_name='Testni holati(Tugatildi/Ishlanmoqda)')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('questions', models.ManyToManyField(to='student.archivequestion', verbose_name='Testda tushgan savollar')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.test')),
            ],
            options={
                'verbose_name': 'Test natija',
                'verbose_name_plural': 'Test natijalar oynasi',
            },
        ),
        migrations.CreateModel(
            name='Recourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nomi')),
                ('file', models.FileField(upload_to='Recourses/', verbose_name='File')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('group', models.ManyToManyField(to='student.group', verbose_name='Qaysi guruhlar uchun')),
                ('science', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.science', verbose_name='Qaysi fandan')),
            ],
            options={
                'verbose_name': 'Manba',
                'verbose_name_plural': 'Manbalar',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='science',
            field=models.ManyToManyField(to='student.science', verbose_name='Fanlar'),
        ),
    ]
