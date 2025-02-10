from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    prerequisites = models.TextField(blank=True, null=True)
    instructor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    pdf_material = models.FileField(upload_to='course_pdfs/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.id} - {self.title}"

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()  # CKEditor field
    video_url = models.URLField(blank=True, null=True)
    pdf_material = models.FileField(upload_to='course_pdfs/', blank=True, null=True)

    def __str__(self):
        return self.title

class MCQQuestion(models.Model):
    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE, related_name="mcqs")
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    explanation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.question_text
    

class register_model(models.Model):
    username=RichTextField()
    email=models.EmailField()
    passw=models.CharField(max_length=40)
    cpassw=models.CharField(max_length=40)
    phone_no=models.CharField(max_length=100,blank=True,null=True)
    Address=models.CharField(max_length=100,blank=True,null=True)
    pincode_no=models.CharField(max_length=10,blank=True,null=True)
    date_of_birth=models.CharField(max_length=20,blank=True,null=True)
    Bio=models.CharField(max_length=200,blank=True,null=True)
    image_ed=models.ImageField(upload_to="data",blank=True,null=True)
      # Track purchased courses
    # purchased_courses = models.ManyToManyField('Course', blank=True)
    purchased_courses = models.ManyToManyField(Course, blank=True) 

    def __str__(self):
        return f"{self.id} - {self.email}"
    

# track complete lessons
class UserLessonCompletion(models.Model):
    user = models.ForeignKey(register_model, on_delete=models.CASCADE)  # Now using RegisterModel
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'lesson')  # Prevent duplicate entries


# test after completion
class FinalTest(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

