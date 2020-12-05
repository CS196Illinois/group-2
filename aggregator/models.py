from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Course Fields 
# Example:
#     name : Discussion
#     hyperlink : zoom.com/here 
class CourseField(models.Model):
    name = models.CharField(max_length=20)
    hyperlink = models.URLField()
    private = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Instructor(models.Model):
    last_name = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    department = models.CharField(max_length=3, help_text="Instructor's department. e.g. CS, ECE, ENG")

    def __str__(self):
        return f'({self.department}) {self.first_name}, {self.last_name}'


class Course(models.Model):
    # Course Descriptors
    title = models.CharField(max_length=25)
    course_number = models.CharField(max_length=10, blank=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)
    section = models.CharField(max_length=5, blank=True)
    created_on = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    fields = models.ManyToManyField(  # This is where we'll have the fields like discussion links, lab links, etc.
        CourseField,
    )
    users = models.ManyToManyField(User)

    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title
