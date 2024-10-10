from django.shortcuts import render,HttpResponse,redirect
from datauploader.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserRegistrationForm,UserLoginForm,UserProfileForm
# from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            return redirect('usersApp:login')  
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'usersPage/signup.html', {'form': form})

def loginHere(request):
    form  = UserLoginForm()
    if request.method=="POST":
        form  = UserLoginForm(request.POST)
        if form.is_valid():
            x = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if x:
                login(request,x)
                return redirect('usersApp:home')
            return HttpResponse('please correct details')
        return HttpResponse('please fill all details')
    form  = UserLoginForm()
    return render(request,'usersPage/login.html',{'form':form})

def logoutHere(request):
    logout(request)
    return redirect('usersApp:login')


@login_required(login_url='usersApp:login')
def homeView(request):
    randomCourses = Courses.objects.order_by('?')[:3]
    return render(request,'usersPage/home.html',{'data':randomCourses})




@login_required(login_url='usersApp:login')
def coursesView(request):
    cart_items = CoursesCart.objects.filter(userId=request.user)
    enroll_items = EnroledCourses.objects.filter(userId=request.user)
    enrolled_courses = [item.courseId.id for item in enroll_items]
    cart_courses = [item.courseId.id for item in cart_items]
    data = Courses.objects.all()
    return render(request,'usersPage/courses.html',{ 'data':data,'cart_list':cart_courses,'enroll_list':enrolled_courses})


@login_required(login_url='usersApp:login')
def addToCartView(request,id):
    course = Courses.objects.get(id=id)
    cartCourse,created = CoursesCart.objects.get_or_create(userId=request.user,courseId=course)
    if  created:
        cartCourse.save()
        return redirect('usersApp:User_courses')
    else:
        
        return redirect('usersApp:User_courses')
    

@login_required(login_url='myapp:login')
def cartView(request):
    data = CoursesCart.objects.filter(userId=request.user)
    total = sum(item.courseId.coursePrice for item in data)
    context = {
        'data': data,
        'total': total
    }
    return render(request,'usersPage/cart.html',context=context)


@login_required(login_url='myapp:login')
def deleteCartItemView(request,id):
    cartItem = CoursesCart.objects.get(id=id)
    cartItem.delete()
    return redirect('usersApp:cart')


@login_required(login_url='usersApp:login')
def AccountView(request):
    user = request.user
    data = CustomUser.objects.get(id=user.id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.middle_name = form.cleaned_data['middle_name']  
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.number = form.cleaned_data['number']
            user.city = form.cleaned_data['city']
            user.age = form.cleaned_data['age']
            user.occupation = form.cleaned_data['occupation']
            user.save()
            return redirect('usersApp:account')
    
    return render(request, 'usersPage/account.html', {'data': data})


@login_required(login_url='usersApp:login')
def enrollCourse(request,id):
    course = Courses.objects.get(id=id)
    enrollCourse,created = EnroledCourses.objects.get_or_create(userId=request.user,courseId=course)
    cart_item = CoursesCart.objects.filter(userId=request.user,courseId=course)
    if cart_item:
        cart_item.delete()
    if  created:
        enrollCourse.save()
        return redirect('usersApp:User_courses')
    else:
        return redirect('usersApp:User_courses')
    


@login_required(login_url='myapp:login')
def enrolledcoursesView(request):
    data = EnroledCourses.objects.filter(userId=request.user)
    return render(request,'usersPage/enrolledcourses.html',{'enrolled_courses':data})


@login_required(login_url='myapp:login')
def checkoutCartCourses(request):
    data = CoursesCart.objects.filter(userId=request.user)
    total = sum(item.courseId.coursePrice for item in data)
    context = {
        'data': data,
        'total': total
    }
    if request.method =='POST':
        for course in data:
            EnroledCourses.objects.create(userId=request.user,courseId=course.courseId)
        data.delete()
        return redirect('usersApp:enrolledcourses')
    return render(request,'usersPage/checkoutPage.html',context=context)


@login_required(login_url='myapp:login')
def checkoutSingleCourses(request,id):
    data = Courses.objects.filter(id=id)
    total = data[0].coursePrice
    context = {
        'data': data,
        'total': total
    }
    if request.method =='POST':
        for course in data:
            EnroledCourses.objects.create(userId=request.user,courseId=course)
            cartCourse =CoursesCart.objects.filter(userId=request.user,courseId=course)
            if cartCourse.exists():
                cartCourse.delete()

        return redirect('usersApp:enrolledcourses')
    return render(request,'usersPage/checkoutPage.html',context=context)
