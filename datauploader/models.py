from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=15, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True, default=0)
    city = models.CharField(max_length=100, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.username

class CourseConcepts(models.Model):
    courseConcept = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.courseConcept

class Courses(models.Model):
    courseName = models.CharField(max_length=60)
    courseImg = models.ImageField(upload_to='images/')
    courseBy = models.CharField(max_length=60)
    coursePrice = models.IntegerField()
    courseDescription = models.CharField(max_length=400)
    conceptList = models.ManyToManyField(CourseConcepts)
    

    def __str__(self) -> str:
        return self.courseName
    
class CoursesCart(models.Model):
    userId = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    courseId = models.ForeignKey(Courses,on_delete=models.CASCADE)


class EnroledCourses(models.Model):
    userId = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    courseId = models.ForeignKey(Courses,on_delete=models.CASCADE)