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
]
