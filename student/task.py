from datetime import timedelta, datetime
from django.utils import timezone
from .models import Student, Result, Test
from django.contrib.auth.models import User


def task_function_for_complete_test(user, test_id, force=False):
    try:
        student = Student.objects.get(user=user)
        for result in Result.objects.filter(student=student):
            if not result.finished and (timezone.now() > result.date + timedelta(hours=result.duration.hour, minutes=result.duration.minute, seconds=result.duration.second) or force):
                correct_answer_number = 0
                count = 0
                for question in result.questions.all():
                    count+=1
                    if question.correct==question.choosen: correct_answer_number+=1
                result.result = f'{correct_answer_number} / {count}'
                test = Test.objects.get(id=test_id)
                if test.required and test.answers>correct_answer_number: result.status = False
                result.finished = True
                if force:
                    t = str(timezone.now() - result.date)
                    result.duration = datetime.strptime(t, '%H:%M:%S.%f').time()
                result.save()

    except:
        pass

def admin_check():
    users = User.objects.all()
    tests = Test.objects.all()
    for user in users:
        for test in tests:
            task_function_for_complete_test(user, test.id)