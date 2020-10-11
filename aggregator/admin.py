from django.contrib import admin
from .models import Course, CourseField, Instructor

# Register your models here.
admin.site.register(Course)
admin.site.register(CourseField)
admin.site.register(Instructor)