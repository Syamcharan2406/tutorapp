from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datauploader.models import *
from .serializers import *

@api_view(['GET'])
def api_get_courses_data(request):
    data = Courses.objects.all()
    serializer = CoursesModelSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_get_concepts_data(request):
    data = CourseConcepts.objects.all()
    serializer = ConceptModelSerializer(data, many=True)
    return Response(serializer.data)