from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import CourseForm, CourseConceptsForm
from .models import CourseConcepts, Courses




def CourseUpload(request):
    f = CourseForm()
    if request.method == "POST":
        f1 = CourseForm(request.POST, request.FILES)
        if f1.is_valid():
            f1.save()
            return redirect('datauploader:course_list')
    return render(request, 'coursesAdmin/courseUpload.html', {'form': f})






def conceptUpload(request):
    f = CourseConceptsForm()
    if request.method == "POST":
        f1 = CourseConceptsForm(request.POST)
        if f1.is_valid():
            f1.save()
            return redirect('datauploader:concept_list')
    return render(request, 'coursesAdmin/conceptUpload.html', {'form': f})



def getData(request):
    data = Courses.objects.all()
    return render(request, 'coursesAdmin/courses.html', {'data': data})



def delete_course(request, id):
    course = get_object_or_404(Courses, id=id)
    course.delete()
    return redirect('datauploader:course_list')



def update_course(request, id):
    course = get_object_or_404(Courses, id=id)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('datauploader:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'coursesAdmin/courseUpload.html', {'form': form})



def concept_list(request):
    concepts = CourseConcepts.objects.all()
    return render(request, 'coursesAdmin/concept_list.html', {'concepts': concepts})



def delete_concept(request, id):
    concept = get_object_or_404(CourseConcepts, id=id)
    if request.method == "POST":
        concept.delete()
        return redirect('datauploader:concept_list')
    return render(request, 'coursesAdmin/confirm_delete_concept.html', {'concept': concept})
