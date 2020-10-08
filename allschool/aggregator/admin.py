from django.contrib import admin
from .models import Course, CourseFields

# Register your models here.
admin.site.register(Course)
admin.site.register(CourseFields)