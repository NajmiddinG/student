from django import forms
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from .task import admin_check

class ScienceAdmin(admin.ModelAdmin):
    order = 4
    list_display = ('name', 'date')
    ordering = ('-date',)


class GroupAdminForm(forms.ModelForm):
    num_students = forms.IntegerField(label="O'quvchilar soni", initial=0)

    class Meta:
        model = Group
        fields = '__all__'

class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    def save_model(self, request, obj, form, change):
        obj.save()
        num_students = form.cleaned_data.get('num_students', 0)
        for i in range(num_students):
            username = f'{obj.name.lower().replace(" ", "")}_{i}'
            user = User(username=username)
            user.set_password(username)
            user.save()
            Student.objects.create(user=user, group=obj)
        super().save_model(request, obj, form, change)
    def delete_model(self, request, obj):
        for i in Student.objects.filter(group=obj):
            User.objects.get(id=i.user.id).delete()
        Student.objects.filter(group=obj).delete()
        super().delete_model(request, obj)

# class GroupAdmin(admin.ModelAdmin):
#     order = 3
#     list_display = ('name', 'date')
#     ordering = ('-date',)

class RecourseAdmin(admin.ModelAdmin):
    order = 5
    list_display = ('name', 'date')
    ordering = ('-date',)

class StudentAdmin(admin.ModelAdmin):
    order = 2
    list_display = ('user', 'group', 'pagination')
    ordering = ('group', 'user__first_name')

class VideoAdmin(admin.ModelAdmin):
    order = 6
    list_display = ('name', 'science', 'date')
    ordering = ('-date',)

class SlideAdmin(admin.ModelAdmin):
    order = 7
    list_display = ('name', 'science', 'date')
    ordering = ('-date',)

class QuestionAdmin(admin.ModelAdmin):
    order = 9
    list_display = ('id', 'get_question')
    ordering = ('question',)

class TestAdmin(admin.ModelAdmin):
    order = 8
    list_display = ('name','number', 'start', 'end', 'duration', 'science', 'required')
    ordering = ('-date',)

class ArchiveQuestionAdmin(admin.ModelAdmin):
    order = 11
    list_display = ('id', 'get_question', 'correct', 'choosen')
    ordering = ('question',)

class ResultAdmin(admin.ModelAdmin):
    admin_check()
    order = 10
    list_display = ('test', 'student', 'result', 'status', 'duration', 'finished', 'date')
    ordering = ('-date',)

admin.site.register(Science, ScienceAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Recourse, RecourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Slide, SlideAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(ArchiveQuestion, ArchiveQuestionAdmin)
admin.site.register(Result, ResultAdmin)