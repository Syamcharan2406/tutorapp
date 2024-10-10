from django import forms
from .models import CourseConcepts, Courses
from cloudinary.forms import CloudinaryFileField

class CourseConceptsForm(forms.ModelForm):
    class Meta:
        model = CourseConcepts
        fields = '__all__'

class CourseForm(forms.ModelForm):
    courseImg = CloudinaryFileField()
    class Meta:
        model = Courses
        fields = '__all__'
        widgets = {
            'conceptList': forms.CheckboxSelectMultiple(),
            'courseDescription': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'})
        }



