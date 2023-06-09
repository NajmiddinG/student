from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password
today = timezone.now
from ckeditor.fields import RichTextField
from django.utils.html import format_html, strip_tags


def five_day(): return timezone.now() + timezone.timedelta(days=5)


class Science(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

    class Meta:
        verbose_name = 'Fan'
        verbose_name_plural = 'Fanlar'

class Group(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Guruh nomi")
    science = models.ManyToManyField(Science, verbose_name="Fanlar")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name
    
    class Meta:
        verbose_name = 'Guruh nomi'
        verbose_name_plural = 'Guruhlar'


class Recourse(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nomi')
    file = models.FileField(upload_to='Recourses/', verbose_name='File')
    group = models.ManyToManyField(Group, verbose_name='Qaysi guruhlar uchun')
    science = models.ForeignKey(Science, on_delete=models.CASCADE, verbose_name='Qaysi fandan')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

    class Meta:
        verbose_name = 'Manba'
        verbose_name_plural = 'Manbalar'


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='User/', blank=True, null=True, verbose_name="Rasm")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Manzil")
    birth_day = models.DateField(blank=True, null=True, verbose_name="Tug'ilgan kun")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Tel")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Guruhi")
    pagination = models.IntegerField(default=10)

    def __str__(self): 
        return f"{self.user.username} {self.user.first_name}"
    
    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"


class Video(models.Model):
    name = models.CharField(max_length=255, verbose_name="Video nomi")
    image = models.ImageField(upload_to='Video/', verbose_name="Video uchun rasm")
    link = models.URLField(default='https://youtube.com', verbose_name="Video linki")
    text = RichTextField(verbose_name="Video uchun post yozing")
    group = models.ManyToManyField(Group, verbose_name="Qaysi guruhlarga tegishli")
    science = models.ForeignKey(Science, on_delete=models.CASCADE, verbose_name="Qaysi fanga tegishli")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videolar'


class Slide(models.Model):
    name = models.CharField(max_length=255, verbose_name='Slide nomi')
    image = models.ImageField(upload_to='Slides/', verbose_name="Rasm")
    text = RichTextField(verbose_name="Slide uchun matn")
    group = models.ManyToManyField(Group, verbose_name="Qaysi guruhlar uchun")
    science = models.ForeignKey(Science, on_delete=models.CASCADE, verbose_name="Qaysi fanga doir")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.name

    class Meta:
        verbose_name = 'Slide'
        verbose_name_plural = 'Slidelar'


class Question(models.Model):
    question = RichTextField(verbose_name="Savol")
    answer = RichTextField(verbose_name="To'gri javob")
    option1 = RichTextField()
    option2 = RichTextField()
    option3 = RichTextField()

    def get_question(self):
        return format_html(self.question)

    def __str__(self):
        return (format_html(f'{self.id}' + " - ") + format_html(self.question))

    class Meta:
        verbose_name = 'Savollar'
        verbose_name_plural = 'Savollar'

class Test(models.Model):
    name = models.CharField(verbose_name="Test nomi", max_length=255)
    number = models.IntegerField(verbose_name="Nechta savol ishlash kerak", default=10)
    start = models.DateTimeField(verbose_name="Qachon boshlanadi", default=today)
    end = models.DateTimeField(verbose_name="Qachon tugaydi", default=five_day)
    duration = models.TimeField(verbose_name="Qancha vaqt davom etadi")
    groups = models.ManyToManyField(Group, verbose_name="Qaysi guruhlar uchun")
    science = models.ForeignKey(Science, verbose_name="Qaysi fandan", on_delete=models.CASCADE)
    required = models.BooleanField(verbose_name="Majburiymi", default=False)
    questions = models.ManyToManyField(Question, verbose_name="Savollar")
    possibilities = models.IntegerField(verbose_name="Imkoniyatlar soni", default=1)
    answers = models.IntegerField(verbose_name="Minimal nechta savolni ishlash to'g'ri topishi", default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ArchiveQuestion(models.Model):
    question = RichTextField(verbose_name='Savol')
    option1 = RichTextField()
    option2 = RichTextField()
    option3 = RichTextField()
    option4 = RichTextField()
    correct = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="To'g'ri javob")
    choosen = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], default=0, verbose_name="O'quvchi tanlagan javob")

    def get_question(self):
        return format_html(self.question)

    def __str__(self):
        return (format_html(f'{self.id}' + " - ") + format_html(self.question))

    class Meta:
        verbose_name = 'Testda tushgan savollar'
        verbose_name_plural = 'Testda tushgan savollar'

class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    result = models.CharField(max_length=100, verbose_name='Natija', null=True, blank=True)
    status = models.BooleanField(default=True, verbose_name="Holati(Tesdan o'tdi/o'tmadi)")
    duration = models.TimeField(verbose_name="Qancha vaqt davom etgani")
    questions = models.ManyToManyField(ArchiveQuestion, verbose_name="Testda tushgan savollar")
    finished = models.BooleanField(default=False, verbose_name="Testni holati(Tugatildi/Ishlanmoqda)")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self): return str(self.finished)

    class Meta:
        verbose_name = 'Test natija'
        verbose_name_plural = 'Test natijalar oynasi'
