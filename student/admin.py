from django import forms
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from .task import admin_check

class ScienceAdmin(admin.ModelAdmin):
    order = 4
    list_display = ('name', 'date')
    ordering = ('-date',)

class RecourseAdmin(admin.ModelAdmin):
    order = 5
    list_display = ('name', 'date')
    ordering = ('-date',)

class StudentAdmin(admin.ModelAdmin):
    order = 2
    list_display = ('user', 'pagination')
    ordering = ('user__first_name',)

class QuestionAdmin(admin.ModelAdmin):
    order = 9
    list_display = ('id', 'get_question')
    ordering = ('question',)

class TestAdmin(admin.ModelAdmin):
    order = 8
    list_display = ('name','number', 'start', 'end', 'duration', 'science')
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
admin.site.register(Student, StudentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(ArchiveQuestion, ArchiveQuestionAdmin)
admin.site.register(Result, ResultAdmin)

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subject', 'percent', 'total_question')
    search_fields = ('user__username', 'subject__name')

