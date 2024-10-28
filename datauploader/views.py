from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import CourseForm, CourseConceptsForm
from .models import CourseConcepts, Courses
from django.views.generic import ListView,DetailView,DeleteView,CreateView,UpdateView
from datauploader.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test,login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.hashers import make_password

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

@login_required(login_url='myapp:login')
@user_passes_test(lambda user: user.is_staff)
def CourseUpload(request):
    f = CourseForm()
    if request.method == "POST":
        f1 = CourseForm(request.POST, request.FILES)
        if f1.is_valid():
            f1.save()
            return redirect('datauploader:course_list')
    return render(request, 'coursesAdmin/courseUpload.html', {'form': f})





@login_required(login_url='myapp:login')
@user_passes_test(lambda user: user.is_staff)
def conceptUpload(request):
    f = CourseConceptsForm()
    if request.method == "POST":
        f1 = CourseConceptsForm(request.POST)
        if f1.is_valid():
            f1.save()
            return redirect('datauploader:concept_list')
    return render(request, 'coursesAdmin/conceptUpload.html', {'form': f})

@login_required(login_url='myapp:login')
@user_passes_test(lambda user: user.is_staff)
def getData(request):
    data = Courses.objects.all()
    return render(request, 'coursesAdmin/courses.html', {'data': data})

@login_required(login_url='myapp:login')
@user_passes_test(lambda user: user.is_staff)
def delete_course(request, id):
    course = get_object_or_404(Courses, id=id)
    course.delete()
    return redirect('datauploader:course_list')

@login_required(login_url='myapp:login')
@user_passes_test(lambda user: user.is_staff)
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

@login_required(login_url='myapp:login')
@user_passes_test(lambda user: user.is_staff)
def concept_list(request):
    concepts = CourseConcepts.objects.all()
    return render(request, 'coursesAdmin/concept_list.html', {'concepts': concepts})

@login_required(login_url='myapp:login')
@user_passes_test(lambda user: user.is_staff)
def delete_concept(request, id):
    concept = get_object_or_404(CourseConcepts, id=id)
    if request.method == "POST":
        concept.delete()
        return redirect('datauploader:concept_list')
    return render(request, 'coursesAdmin/confirm_delete_concept.html', {'concept': concept})


class UsersData(ListView,StaffRequiredMixin,LoginRequiredMixin):
    model = CustomUser
    template_name = 'coursesAdmin/userDetails.html'
    paginate_by = 10
    
    def get_queryset(self):
        return CustomUser.objects.all().order_by('-date_joined')
    


class UserCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = CustomUser
    template_name = 'coursesAdmin/userform.html'
    fields = ['username', 'first_name', 'middle_name', 'last_name', 'email', 
              'number', 'age', 'city', 'occupation', 'is_active', 'is_staff', 
              'is_superuser', 'password']
    success_url = reverse_lazy('datauploader:user_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Make password field use password input type
        form.fields['password'].widget.input_type = 'password'
        # Add Bootstrap classes to all fields
        for field in form.fields:
            form.fields[field].widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        # Hash the password before saving
        form.instance.password = make_password(form.cleaned_data['password'])
        messages.success(self.request, f'User {form.instance.username} has been created successfully.')
        return super().form_valid(form)
    

class UserUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'coursesAdmin/userform.html'
    fields = ['username', 'first_name', 'middle_name', 'last_name', 'email', 
              'number', 'age', 'city', 'occupation', 'is_active', 'is_staff', 
              'is_superuser']
    success_url = reverse_lazy('datauploader:user_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Add Bootstrap classes to all fields
        for field in form.fields:
            form.fields[field].widget.attrs.update({'class': 'form-control'})
        return form

    def form_valid(self, form):
        messages.success(self.request, f'User {form.instance.username} has been updated successfully.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

class UserDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('datauploader:user_list')
    template_name = 'coursesAdmin/userConfirmDelete.html'
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        messages.success(request, f'User {user.username} has been deleted successfully.')
        return super().delete(request, *args, **kwargs)