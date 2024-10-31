from django.urls import path
from .views import *

app_name = 'datauploader'

urlpatterns = [
    path('courses/', getData, name='course_list'),
    path('course/upload/', CourseUpload, name='course_upload'),
    path('concept/upload/', conceptUpload, name='concept_upload'),
    path('course/delete/<int:id>/', delete_course, name='delete_course'),
    path('course/update/<int:id>/', update_course, name='update_course'),
    path('concept/delete/<int:id>/', delete_concept, name='delete_concept'),
    path('concepts/', concept_list, name='concept_list'),
    path('users/', UsersData.as_view(), name='user_list'),
    path('ajax-user-search/', ajax_user_search, name='ajax-user-search'),
    path('user/<int:pk>/edit/', UserUpdateView.as_view(), name='edit-user'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='delete-user'),
    path('user/add/', UserCreateView.as_view(), name='add-user'),
]
