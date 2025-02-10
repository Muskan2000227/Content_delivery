from django.shortcuts import render, get_object_or_404,redirect
from .models import Course, Module, Lesson,MCQQuestion,FinalTest
import stripe
from django.conf import settings
import random

def course_list(request):
    courses = Course.objects.all()
    user_email = request.session.get('user_email')
    return render(request, 'course_list.html', {'courses': courses,'email':user_email})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Course,register_model, UserLessonCompletion, Lesson

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = course.module_set.all()

    # ✅ Check if the user has purchased the course
    user_has_purchased = False
    user_email = request.session.get('user_email')

    if request.user.is_authenticated:
        try:
            user_record = register_model.objects.get(email=user_email)
            user_has_purchased = user_record.purchased_courses.filter(id=course.id).exists()

            # ✅ Count total lessons in the course
            total_lessons = Lesson.objects.filter(module__course=course).count()
            print(f"Total Lessons in Course {course_id}: {total_lessons}")
            # ✅ Count completed lessons for the user
            completed_lessons = UserLessonCompletion.objects.filter(
                user=user_record, lesson__module__course=course, completed=True
            ).count()
            print(f"Completed Lessons by User {user_email}: {completed_lessons}") 

            # ✅ Check if all lessons are completed
            all_completed = completed_lessons == total_lessons

        except register_model.DoesNotExist:
            all_completed = False  # Default to False if user not found

        return render(request, "course_detail.html", {
        "course": course,
        "modules": modules,
        "user_has_purchased": user_has_purchased,
        "all_completed": all_completed,
        "total_lessons": total_lessons  # ✅ Pass lesson count to template
        })



# def course_detail(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     modules = course.module_set.all()

#     # Check if user has purchased the course
#     user_has_purchased = False
#     user_email = request.session.get('user_email')
#     if request.user.is_authenticated:
#         try:
#             user_record = register_model.objects.get(email=user_email)
#             user_has_purchased = user_record.purchased_courses.filter(id=course.id).exists()
#         except register_model.DoesNotExist:
#             pass  # If user record doesn't exist, default to False

#     return render(request, "course_detail.html", {
#         "course": course,
#         "modules": modules,
#         "user_has_purchased": user_has_purchased
#     })

def module_detail(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    lessons = module.lesson_set.all()  # Get all lessons for this module
    return render(request, 'module_detail.html', {'module': module, 'lessons': lessons})

# for random mcq 
# import random
# def lesson_detail(request, lesson_id):
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     all_mcqs = list(MCQQuestion.objects.filter(lesson=lesson))  # Get all questions for the lesson
#     random.shuffle(all_mcqs)  # Shuffle the list randomly
#     selected_mcqs = all_mcqs[:10]  # Pick first 10 random questions

#     return render(request, 'lesson_detail.html', {
#         'lesson': lesson,
#         'mcqs': selected_mcqs
#     })


# from django.shortcuts import render, get_object_or_404
# from .models import Lesson, MCQQuestion

# def lesson_detail(request, lesson_id):
#     lesson = get_object_or_404(Lesson, id=lesson_id)
#     mcqs = lesson.mcqs.all()  # Fetch MCQs related to this lesson
#     return render(request, 'lesson_detail.html', {'lesson': lesson, 'mcqs': mcqs})




def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    mcqs = lesson.mcqs.all()
    # ✅ Check if user is authenticated
    if request.user.is_authenticated:
        user_email = request.session.get('user_email')
        user_record = register_model.objects.filter(email=user_email).first()

        if user_record:
            # ✅ Mark lesson as completed
            completion, created = UserLessonCompletion.objects.get_or_create(
                user=user_record, lesson=lesson
            )
            if not completion.completed:
                completion.completed = True
                completion.save()

    return render(request, "lesson_detail.html", {"lesson": lesson,'mcqs': mcqs})






def home(request):
    return render(request, 'base.html')

from .models import register_model  # Ensure your model is imported
from django.contrib import messages

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        confirm_password = request.POST.get('cpass')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')

        if register_model.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'signup.html')

        # Create new user
        register_model.objects.create(username=username, email=email, passw=password)
        messages.success(request, "Signup successful! You can now login.")
        return redirect('login')  # Redirect to the login page

    return render(request, 'signup.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import register_model  # Import your user model

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('passw')  # Ensure field name matches your model

        try:
            user = register_model.objects.get(email=email)
            request.session['user_email'] = email 
            if user.passw == password:  # Plaintext comparison (since no hashing was used in signup)
                request.session['user_id'] = user.id  # Store user ID in session
                messages.success(request, "Login successful!")
                return redirect('course_list')  # Redirect to the home page or dashboard
            else:
                messages.error(request, "Invalid password")
        except register_model.DoesNotExist:
            messages.error(request, "Email not registered")

    return render(request, 'login.html')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']  # Remove user session
        messages.success(request, "You have been logged out successfully!")
    return redirect('login')  # Redirect to the login page


def mainpage(request):
    courses = Course.objects.all()
    return render(request, 'mainpage.html', {'courses': courses})






stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, course_id):
    course = Course.objects.get(id=course_id)
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': course.title,
                },
                'unit_amount': 1000,  # $10.00 in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f"http://127.0.0.1:8000/payment-success/{course_id}/",
        cancel_url="http://127.0.0.1:8000/payment-failed/",
    )
    
    return redirect(session.url)


def payment_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Try to find user by session or manually retrieve email
    user_email = request.session.get('user_email')  # Check session if email is stored
    if not user_email:
        return render(request, "payment_failed.html", {"error": "User email not found"})

    user = get_object_or_404(register_model, email=user_email)
    
    # Add course to purchased courses
    user.purchased_courses.add(course)
    
    return render(request, "payment_success.html", {"course": course})

# def payment_success(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     user = request.user  

#     # Get the user record from register_model
#     try:
#         user_record = register_model.objects.get(email=user.email)
#     except register_model.DoesNotExist:
#         return redirect('course_list')  # Handle case where user is not found

#     # Add the purchased course if not already added
#     if course not in user_record.purchased_courses.all():
#         user_record.purchased_courses.add(course)
#         user_record.save()

#     return render(request, "payment_success.html", {"course": course})




# To show all the buyed courses
from django.shortcuts import render
from .models import register_model

def purchased_courses(request):
    user_email = request.session.get('user_email')
    if request.user.is_authenticated:
        user = register_model.objects.get(email=user_email)
        purchased_courses = user.purchased_courses.all().order_by('-id')  # Get only the courses the user has purchased
    else:
        purchased_courses = []

    return render(request, 'purchased_courses.html', {'purchased_courses': purchased_courses})


def index(request):
    return render(request,'index.html')


from django.http import JsonResponse
def complete_lesson(request, lesson_id):
    if request.user.is_authenticated:
        user = request.user
        lesson = get_object_or_404(Lesson, id=lesson_id)

        # Try to find an existing completion record
        completion, created = UserLessonCompletion.objects.get_or_create(user=user, lesson=lesson)
        
        # Update completion status
        if not completion.completed:
            completion.completed = True
            completion.save()

        return JsonResponse({"status": "success", "message": "Lesson marked as completed!"})
    
    return JsonResponse({"status": "error", "message": "User not authenticated."})




def final_test(request, course_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(register_model, id=user_id)

    # ✅ Corrected: Filter by `course_id`, not `module_id`
    questions = list(FinalTest.objects.filter(course_id=course_id))  
    random.shuffle(questions)  # Shuffle questions

    return render(request, 'final_test.html', {'questions': questions[:10]})