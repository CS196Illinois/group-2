from django.shortcuts import render
from aggregator.models import CourseField, Course, Instructor
from django.contrib.auth import logout
from django.contrib import messages
from .forms import CourseForm, InstructorForm, FieldForm

# Create your views here.
def index(request):
    current_user = request.user
    courses = Course.objects.all()
    context = {
        'courses' : courses,
    }
    return render(request, 'index.html', context=context)

def user_logout(request):
    logout(request)
    courses = Course.objects.all()
    context = {
        'courses' : courses,
    }
    return render(request, 'index.html', context=context)

def add_course(request):
    courseForm = CourseForm(request.POST or None)
    instructForm = InstructorForm(request.POST or None)
    fieldForm = FieldForm(request.POST or None)
    instructors = Instructor.objects.all()
    context = {
        'courseForm' : courseForm,
        'instructForm' : instructForm,
        'fieldForm' : fieldForm,
        'instructors': instructors,
    }
    if courseForm.is_valid():
        courseForm.save()
        #note from Larry: we should add an alert or message to the page confirming that a course was added to the database
        #probably use combination of css + javascript?
        return index(request) #redirects to home page

    if instructForm.is_valid():
        instructForm.save()
        #note from Larry: we should add an alert or message to the page confirming that an intructor was added to the database
        #probably use combination of css + javascript?

    if fieldForm.is_valid():
        fieldForm.save()
        #note from Larry: we should add an alert or message to the page confirming that a CourseField was added to the databsae
        #probably use combination of css + javascript?

    return render(request, 'course_form.html', context)

def about(request):
    return render(request, 'about.html')

