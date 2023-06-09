from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import  Science, Group, Recourse, Student, Video, Slide, Question, Test, ArchiveQuestion, Result
from .serializers import (UserSerializer, ScienceSerializer, GroupSerializer, RecourseSerializer, StudentSerializer, VideoSerializer, SlideSerializer, QuestionSerializer, TestSerializer, ArchiveQuestionSerializer, ResultSerializer, ResultViewSerializer)
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from datetime import datetime, timedelta
from django.utils import timezone
from django.core import serializers
import random
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from .task import task_function_for_complete_test


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        student = Student.objects.filter(user=user).first()
        if student:
            token['student_id'] = student.id
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def update_student(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        student = Student.objects.get(user=user)
    except User.DoesNotExist:
        return Response(status=404)
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.save()

    
    if student is not None:
        student.location = request.data.get('location', student.location)
        student.birth_day = request.data.get('birth_day', student.birth_day)
        student.phone = request.data.get('phone', student.phone)
        image_file = request.data.get('image')
        if image_file is not None:
            filename = f"{user_id}_{image_file.name}"
            student.image.save(filename, ContentFile(image_file.read()))
        student.save()

    return Response(status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def video_list(request):
    try:
        user_group = Student.objects.get(user=request.user).group
        videos = Video.objects.filter(group=user_group)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def video_detail(request, id):
    try:
        user_group = Student.objects.get(user=request.user).group
        video = Video.objects.get(id=id, group=user_group)
        serializer = VideoSerializer(video)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated, IsAdminUser])
# @authentication_classes([JWTAuthentication])
# def create_test(request):
#     if request.user.is_staff:
#         # create test in here
#         return Response({'message': 'Welcome, admin!'})
#     else:
#         return Response({'message': 'You are not authorized to access this endpoint.'}, status=403)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def list_of_tests(request, science):
    try:
        user_group = Student.objects.get(user=request.user).group
        tests = Test.objects.filter(groups=user_group, science=science)
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def test_detail(request, test_id):
    try:
        student = Student.objects.get(user=request.user)
        user_group = Student.objects.get(user=request.user).group
        test_obj = Test.objects.get(id=test_id)
        find = False
        for gr in test_obj.groups.all():
            if gr==user_group:
                find = True
                break
        if not find: return Response({'error': "This user cannot use this test!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        additional_data = {
            'test_is_in_progress': True,
        }
        task_function_for_complete_test(request.user, test_id)
        if test_obj.end <= timezone.now(): additional_data['test_is_in_progress'] = False
        else:
            archive = Result.objects.filter(test_id=test_id, student_id=student.id, finished=False).first()
            if archive: additional_data['started_test_id'] = archive.id
        
        additional_data['overall_started_number'] = Result.objects.filter(test_id=test_id, student_id=student.id, finished=True).count()
        if Result.objects.filter(test_id=test_id, student=student, finished=True).count()>0:
            additional_data['oxirgi_ishlangan_testni_natijasi_uchun_result_id'] = Result.objects.filter(test_id=test_id, student=student, finished=True).order_by('-date').first().id
        data = {
            'test': TestSerializer(test_obj).data,
            'additional_data': additional_data,
        }
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def start_new_test(request, test_id):
    try:
        student = Student.objects.get(user=request.user)
        user_group = Student.objects.get(user=request.user).group
        test_obj = Test.objects.get(id=test_id)
        find = False
        for gr in test_obj.groups.all():
            if gr==user_group:
                find = True
                break
        if not find: return Response({'error': "This user cannot use this test!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if test_obj.end <= timezone.now(): return Response({'error': "This test is finished."}, status=status.HTTP_423_LOCKED)
        elif Result.objects.filter(test_id=test_id, student_id=student.id, finished=False).exists(): return Response({'error': "You have incomplete test, pleese complete this test first. Then you can try again if you have opportunities!"}, status=status.HTTP_102_PROCESSING)
        
        count = Result.objects.filter(test_id=test_id, student_id=student.id, finished=True).count()
        if count>=test_obj.possibilities: return Response({'error': "You have no new oportunity to start new test!"}, status=status.HTTP_403_FORBIDDEN)

       # Create test
        questions = list(test_obj.questions.all())
        random_items = random.sample(questions, test_obj.number)
        archive_questions = []
        for item in random_items:
            correct = random.randint(1, 4)
            q = {'question': item.question}
            if correct == 1:
                q['option1'] = item.answer
                q['option2'] = item.option1
                q['option3'] = item.option2
                q['option4'] = item.option3
            elif correct == 2:
                q['option2'] = item.answer
                q['option1'] = item.option1
                q['option3'] = item.option2
                q['option4'] = item.option3
            elif correct == 3:
                q['option3'] = item.answer
                q['option2'] = item.option1
                q['option1'] = item.option2
                q['option4'] = item.option3
            else:
                q['option4'] = item.answer
                q['option2'] = item.option1
                q['option3'] = item.option2
                q['option1'] = item.option3
            
            q['correct'] = correct
            archive_question = ArchiveQuestion.objects.create(question=q['question'],option1=q['option1'], option2=q['option2'], option3=q['option3'], option4=q['option4'], correct=correct)
            archive_questions.append(archive_question)


        remaining_time = (test_obj.end - timezone.now()).total_seconds()
        test_duration = timedelta(hours=test_obj.duration.hour, minutes=test_obj.duration.minute, seconds=test_obj.duration.second).total_seconds()
        if test_duration<=remaining_time: duration = test_obj.duration
        else: duration = timedelta(hours=remaining_time//3600, minutes=remaining_time%3600//60, seconds=remaining_time%60)
        result = Result.objects.create(test_id=test_id, student=student, duration=duration)
        result.questions.set(archive_questions)
        result.save()
        serialized_result = ResultSerializer(result)
        return Response(serialized_result.data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def submit_test(request, result_id):
    test_id = Result.objects.get(id=result_id).test.id
    user_group = Student.objects.get(user=request.user).group
    test_obj = Test.objects.get(id=test_id)
    find = False
    for gr in test_obj.groups.all():
        if gr==user_group:
            find = True
            break
    if not find: return Response({'error': "This user cannot use this test!"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if Result.objects.get(id=result_id).finished: return Response({'error': 'This test is already finished'})
    task_function_for_complete_test(user=request.user, test_id=test_id, force=True)
    return Response(ResultSerializer(Result.objects.get(id=result_id)).data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_choosen_test_option(request, archive_question_id, choosen):
    try:
        a = ArchiveQuestion.objects.get(id=archive_question_id)
        a.choosen=choosen
        a.save()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RecourceViewSet(viewsets.ViewSet):
    serializer_class = RecourseSerializer

    @permission_classes([IsAuthenticated])
    @authentication_classes([JWTAuthentication])
    def retrieve(self, request, pk=None):
        queryset = Recourse.objects.filter(science=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ScienceViewSet(viewsets.ModelViewSet):
    queryset = Science.objects.all()
    serializer_class = ScienceSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class SlideViewSet(viewsets.ModelViewSet):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class ArchiveQuestionViewSet(viewsets.ModelViewSet):
    queryset = ArchiveQuestion.objects.all()
    serializer_class = ArchiveQuestionSerializer


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class ResultViewViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultViewSerializer
