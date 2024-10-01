from django import forms
from .models import CourseConcepts, Courses


class CourseConceptsForm(forms.ModelForm):
    class Meta:
        model = CourseConcepts
        fields = '__all__'

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = '__all__'
        widgets = {
            'conceptList': forms.CheckboxSelectMultiple(),
            'courseDescription' : forms.Textarea(attrs={'rows' : 5,'cols':180})
        }


