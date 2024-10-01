from django.urls import path
from .views import *
app_name = 'usersApp'
urlpatterns = [
    path('',loginHere,name='login'),
     path('logout',logoutHere,name='logout'),
    path('home/',homeView,name='home'),
    path('register/', register_view, name='register'),
    path('courses/', coursesView, name='User_courses'),
    path('AddItemTocart/<int:id>', addToCartView, name='AddToCart'),
    path('cart/', cartView, name='cart'),
    path('deleteCartItem/<int:id>', deleteCartItemView, name='delete'),
    path('account/', AccountView, name='account'),
    path('enrollcourse/<int:id>', enrollCourse, name='enroll'),
    path('enrolledcourses/', enrolledcoursesView, name='enrolledcourses'),
    path('checkout/', checkoutCartCourses, name='checkoutCart'),
    path('checkout/<int:id>/', checkoutSingleCourses, name='checkoutSingle'),
    ]