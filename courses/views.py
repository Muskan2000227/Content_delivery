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

# def course_detail(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     modules = course.module_set.all()

#     # ✅ Check if the user has purchased the course
#     user_has_purchased = False
#     user_email = request.session.get('user_email')

#     if request.user.is_authenticated:
#         try:
#             user_record = register_model.objects.get(email=user_email)
#             user_has_purchased = user_record.purchased_courses.filter(id=course.id).exists()

#             # ✅ Count total lessons in the course
#             total_lessons = Lesson.objects.filter(module__course=course).count()
#             print(f"Total Lessons in Course {course_id}: {total_lessons}")
#             # ✅ Count completed lessons for the user
#             completed_lessons = UserLessonCompletion.objects.filter(
#                 user=user_record, lesson__module__course=course, completed=True
#             ).count()
#             print(f"Completed Lessons by User {user_email}: {completed_lessons}") 

#             # ✅ Check if all lessons are completed
#             all_completed = completed_lessons == total_lessons

#         except register_model.DoesNotExist:
#             all_completed = False  # Default to False if user not found

#         return render(request, "course_detail.html", {
#         "course": course,
#         "modules": modules,
#         "user_has_purchased": user_has_purchased,
#         "all_completed": all_completed,
#         "total_lessons": total_lessons  # ✅ Pass lesson count to template
#         })

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = course.module_set.all()

    user_has_purchased = False
    user_email = request.session.get('user_email')

    completed_lesson_ids = []  # ✅ Store completed lesson IDs

    if request.user.is_authenticated:
        try:
            user_record = register_model.objects.get(email=user_email)
            user_has_purchased = user_record.purchased_courses.filter(id=course.id).exists()

            total_lessons = Lesson.objects.filter(module__course=course).count()
            
            completed_lessons = UserLessonCompletion.objects.filter(
                user=user_record, lesson__module__course=course, completed=True
            )

            completed_lesson_ids = list(completed_lessons.values_list("lesson_id", flat=True))  # ✅ Get completed lesson IDs
            print(completed_lesson_ids)
            all_completed = len(completed_lesson_ids) == total_lessons

        except register_model.DoesNotExist:
            all_completed = False  

    return render(request, "course_detail.html", {
        "course": course,
        "modules": modules,
        "user_has_purchased": user_has_purchased,
        "all_completed": all_completed,
        "total_lessons": total_lessons,
        "completed_lesson_ids": completed_lesson_ids  # ✅ Send completed lesson IDs
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




# To show all the bought courses
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


# from django.http import JsonResponse
# def complete_lesson(request, lesson_id):
#     if request.user.is_authenticated:
#         user = request.user
#         lesson = get_object_or_404(Lesson, id=lesson_id)

#         # Try to find an existing completion record
#         completion, created = UserLessonCompletion.objects.get_or_create(user=user, lesson=lesson)
        
#         # Update completion status
#         if not completion.completed:
#             completion.completed = True
#             completion.save()

#         return JsonResponse({"status": "success", "message": "Lesson marked as completed!"})
    
#     return JsonResponse({"status": "error", "message": "User not authenticated."})




# def final_test(request, course_id):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('login')

#     user = get_object_or_404(register_model, id=user_id)

#     # ✅ Corrected: Filter by `course_id`, not `module_id`
#     questions = list(FinalTest.objects.filter(course_id=course_id))  
#     random.shuffle(questions)  # Shuffle questions

#     return render(request, 'final_test.html', {'questions': questions[:10]})

# def final_test(request, course_id):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('login')

#     user = get_object_or_404(register_model, id=user_id)

#     questions = list(FinalTest.objects.filter(course_id=course_id))  
#     random.shuffle(questions)

#     if request.method == "POST":
#         total_questions = len(questions)
#         correct_answers = 0

#         for question in questions:
#             selected_answer = request.POST.get(f"question_{question.id}")
#             if selected_answer == question.correct_option:
#                 correct_answers += 1

#         score_percentage = (correct_answers / total_questions) * 100

#         if score_percentage >= 75:
#             request.session['certified_user'] = user.username  # ✅ Store name in session
#             generate_certificate(user.username)  # ✅ Generate certificate
#             return redirect('certificate_page')  # ✅ Redirect to certificate preview page

#         return render(request, 'final_test.html', {'questions': questions[:10], 'message': "Test not cleared. Try again."})

#     return render(request, 'final_test.html', {'questions': questions[:10]})

from django.utils.html import strip_tags
def final_test(request, course_id):
    user_email = request.session.get('user_email')  
    if not user_email:
        return redirect('login')

    user = get_object_or_404(register_model, email=user_email)  # Fetch user by email

    questions = list(FinalTest.objects.filter(course_id=course_id))  
    random.shuffle(questions)

    if request.method == "POST":
        total_questions = len(questions)
        correct_answers = 0

        for question in questions:
            selected_answer = request.POST.get(f"question_{question.id}")
            if selected_answer == question.correct_option:
                correct_answers += 1

        score_percentage = (correct_answers / total_questions) * 100

        if score_percentage >= 75:
            clean_username = strip_tags(user.username)  # Remove HTML tags if present
            request.session['certified_user'] = clean_username
            generate_certificate(clean_username)
            return redirect('certificate_page')  # Redirect to certificate preview page

        return render(request, 'final_test.html', {'questions': questions})  

    return render(request, 'final_test.html', {'questions': questions})



from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
import os
from .models import register_model, FinalTest
import random

def generate_certificate(user_name):
    """Generate a certificate with the user's name and return a downloadable PDF."""
    template_path = "static/certificate_template.png"  # ✅ Ensure this path is correct
    font_path = "static/font/Roboto-Bold.ttf"  # ✅ Use any suitable font

    # Open the template image
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)

    # Load a font
    font_size = 60
    font = ImageFont.truetype(font_path, font_size)

    # Define text position (Modify based on your template)
    text_position = (700, 700)  

    # Add user's name
    draw.text(text_position, user_name, fill="black", font=font)

    # Save as a temporary file
    # cert_path = f"media/certificates/{user_name}_certificate.png"
    # os.makedirs(os.path.dirname(cert_path), exist_ok=True)
    # img.save(cert_path)

    # Convert to PDF
    pdf_path = f"media/certificates/{user_name}_certificate.pdf"
    img.convert("RGB").save(pdf_path)
    return pdf_path 
    # Return file as response for download
    # with open(pdf_path, "rb") as pdf_file:
    #     response = HttpResponse(pdf_file.read(), content_type="application/pdf")
    #     response["Content-Disposition"] = f'attachment; filename="{user_name}_certificate.pdf"'
    #     return response


def certificate_view(request):
    user_name = request.session.get('certified_user'9)
    # Construct absolute file path
    # cert_file = os.path.join(settings.MEDIA_ROOT, "certificates", f"{user_name}_certificate.pdf")
    # Use MEDIA_URL for correct file serving
    cert_url = f"{settings.MEDIA_URL}certificates/{user_name}_certificate.pdf"
    return render(request, "certificate_page.html", {"user_name": user_name, "cert_path": cert_url})

# from django.core.mail import EmailMessage
# from django.conf import settings

# def certificate_view(request):
#     user_name = request.session.get('certified_user')
#     user_email = request.session.get('user_email')  # Ensure email is stored in the session

#     # Generate the certificate
#     certificate_path = generate_certificate(user_name)  # Ensure this function returns the file path
#     cert_url = f"{settings.MEDIA_URL}certificates/{user_name}_certificate.pdf"

#     # ✅ Send email with attachment
#     subject = "Your Certificate is Ready! 🎉"
#     message = f"""
#     Dear {user_name},

#     Congratulations! 🎉 Your certificate is ready.
#     Best Regards,  
#     Your Organization
#     """

#     email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
#     email.attach_file(certificate_path)  # Attach the certificate PDF
#     email.send()

#     return render(request, "certificate_page.html", {"user_name": user_name, "cert_path": cert_url})

