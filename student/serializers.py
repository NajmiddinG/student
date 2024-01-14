from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Science, Student, Question, Test, ArchiveQuestion, Result, Rank
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = ['id', 'user', 'image', 'location', 'birth_day', 'phone']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise serializers.ValidationError(user_serializer.errors)

        return super().update(instance, validated_data)


class ScienceSerializer(serializers.ModelSerializer):
    tests_count = serializers.SerializerMethodField()
    recourse_count = serializers.SerializerMethodField()
    class Meta:
        model = Science
        fields = '__all__'

    def get_tests_count(self, obj):
        tests = Test.objects.filter(science_id=obj.id)

        return tests.count()


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        exclude = ('questions', 'science') 


class ArchiveQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiveQuestion
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    questions = ArchiveQuestionSerializer(many=True)
    class Meta:
        model = Result
        exclude = ('test', 'student')
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        questions = representation['questions']
        for question in questions:
            question.pop('correct')
        return representation

class ResultViewSerializer(serializers.ModelSerializer):
    questions = ArchiveQuestionSerializer(many=True)
    class Meta:
        model = Result
        exclude = ('test', 'student')

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = '__all__'