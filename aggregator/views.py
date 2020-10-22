from django.shortcuts import render, redirect
from aggregator.models import CourseField, Course, Instructor
from django.contrib.auth import logout
from django.contrib import messages
from .forms import CourseForm, InstructorForm, FieldForm

# Create your views here.
def index(request):
    print('index()')
    if request.user.is_authenticated:
        courses = Course.objects.filter(user=request.user)
    else:
        courses = []
    context = {
        'courses' : courses,
        'authenticated': request.user.is_authenticated,
    }
    return render(request, 'index.html', context=context)

def user_logout(request):
    logout(request)
    return redirect('/aggregator/')

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
    if courseForm.is_valid() and request.user.is_authenticated:
        course = Course(
            title=courseForm.cleaned_data['title'],
            course_number=courseForm.cleaned_data['course_number'],
            instructor=courseForm.cleaned_data['instructor'],
            section=courseForm.cleaned_data['section'],
            user=request.user
        )
        course.save()
        for field in courseForm.cleaned_data['fields']:
            course.fields.add(field)
        course.save()

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

