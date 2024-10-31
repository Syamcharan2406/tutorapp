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
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.template.loader import render_to_string


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

class UsersData(ListView, StaffRequiredMixin, LoginRequiredMixin):
    model = CustomUser
    template_name = 'coursesAdmin/userDetails.html'
    paginate_by = 10
    
    def get_queryset(self):
        return CustomUser.objects.all().order_by('-date_joined')
    
    
@login_required(login_url='myapp:login')
@user_passes_test(lambda user: user.is_staff)
def ajax_user_search(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    if query:
        users = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(number__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(city__icontains=query) |
            Q(occupation__icontains=query)
        ).order_by('-date_joined')
    else:
        users = CustomUser.objects.all().order_by('-date_joined')

    paginator = Paginator(users, 10)  # 10 users per page
    try:
        users_page = paginator.page(page)
    except:
        users_page = paginator.page(1)

    # Render the HTML for the user rows
    user_rows_html = render_to_string('coursesAdmin/table_rows.html', {'object_list': users_page})

    return JsonResponse({
        'user_rows': user_rows_html,  # Returning the rendered HTML instead of user list
        'total_pages': paginator.num_pages,
        'current_page': users_page.number,
        'has_next': users_page.has_next(),
        'has_previous': users_page.has_previous()
    })

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