from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget
from django.db import models


admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(register_model)
admin.site.register(UserLessonCompletion)
admin.site.register(FinalTest)
admin.site.register(MCQQuestion)
