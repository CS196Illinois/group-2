from django.shortcuts import render, redirect
from aggregator.models import CourseField, Course, Instructor
from django.contrib.auth import logout
from django.contrib import messages
from .forms import CourseForm, InstructorForm, FieldForm, CourseSearch

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
        return redirect('/aggregator') #redirects to home page (changed from render to redirect)

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

def loadDetails(request, course_load ):
    course = Course.objects.all().get(title=course_load)
    fieldForm = FieldForm(request.POST or None)

    context = {
        'course' : course,
        'fieldForm' : fieldForm,
    }

    if fieldForm.is_valid():
        newField = CourseField(
            name = fieldForm.cleaned_data['name'],
            hyperlink = fieldForm.cleaned_data['hyperlink']
        )
        newField.save()
        course.fields.add(newField)
        course.save()

    return render(request, 'course_detail.html', context)

def searchPage(request):
    courses = Course.objects.all()
    form = CourseSearch(request.POST or None)
    if form.is_valid():
        query = form.cleaned_data['Search']
        filtered = []
        if len(query) != None and len(query) != 0:
            for course in courses:
                #checks if the query string is in this mashed string of relevant fields to check for
                #should make the search better in the future
                toCheck = course.title + " " + course.course_number + " " + course.instructor.last_name + " " + course.instructor.first_name + " " + course.section + " " + course.instructor.department
                if query.lower() in toCheck.lower():
                    filtered.append(course)
            courses = filtered
    
    context = {
        'courses' : courses,
        'searchForm' : form
    }
    
    return render(request, 'course_search.html', context)