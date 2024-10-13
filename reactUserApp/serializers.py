from rest_framework import serializers
from datauploader.models import *

class CoursesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'



class ConceptModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseConcepts
        fields = '__all__'