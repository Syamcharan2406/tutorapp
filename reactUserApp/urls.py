from django.urls import path
from .views import *
app_name = 'reactUserApp'
urlpatterns = [
    path('courses/',api_get_courses_data,name='api_get_courses_data'),
    path('concepts/',api_get_concepts_data,name='api_get_concepts_data')
]