"""
URL configuration for content_delivery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from courses import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
     # Course URLs
    path('course_list', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),

    # Module URLs
    path('modules/<int:module_id>/', views.module_detail, name='module_detail'),

    # Lesson URLs
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('home', views.home, name='home'),
   
#    Signup
    path('Signup', views.signup, name='signup'),

    # Login
    path('Login', views.login, name='login'),
    # Logout
    path('Logout', views.logout, name='logout'),  
   
    # Mainpage(before login)
    path('main', views.mainpage, name='mainpage'),

    # Stripe
    path('create-checkout-session/<int:course_id>/', views.create_checkout_session, name='create-checkout-session'),
    path('payment-success/<int:course_id>/', views.payment_success, name='payment-success'),

    # Purchased courses
     path('my-courses/', views.purchased_courses, name='purchased_courses'),
 
    # Final Test
    path('final-test/<int:course_id>/', views.final_test, name='final_test'),

    path('certificate/',views.certificate_view, name='certificate_page'), 

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)