from django.urls import path, include
from rest_framework import routers
from .views import (
    UserViewSet,
    ScienceViewSet,
    StudentViewSet,
    QuestionViewSet,
    TestViewSet,
    ResultViewSet,
    update_student, list_of_tests, test_detail, start_new_test, submit_test, add_choosen_test_option,
    MyTokenObtainPairView,
    ResultViewViewSet,
)

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('sciences', ScienceViewSet)
router.register('students', StudentViewSet)
router.register('questions', QuestionViewSet)
router.register('tests', TestViewSet)
router.register('results', ResultViewSet)
router.register('result-views', ResultViewViewSet)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', include(router.urls)),
    path('list-of-tests/<int:science>/', list_of_tests, name='list_of_tests'),
    path('test-detail/<int:test_id>/', test_detail, name='test_detail'),
    path('start-new-test/<int:test_id>/', start_new_test, name='start_new_test'),
    path('submit-test/<int:result_id>/', submit_test, name='submit_test'),
    path('add-choosen-test-option/<int:archive_question_id>/<int:choosen>/', add_choosen_test_option, name='add_choosen_test_option'),
    path('update-student/<int:user_id>/', update_student, name='update_student'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
