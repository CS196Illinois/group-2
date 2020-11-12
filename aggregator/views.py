from django.shortcuts import render, redirect
from aggregator.models import CourseField, Course, Instructor
from django.contrib.auth import logout
from django.contrib import messages
from .forms import CourseForm, InstructorForm, FieldForm, CourseSearch

# Create your views here.
def index(request):
    print('index()')
    courseForm = CourseForm(request.POST or None)
    instructForm = InstructorForm(request.POST or None)
    if request.user.is_authenticated:
        courses =[]
        allCourses = Course.objects.all()
        for item in allCourses:
            if request.user in item.users.all():
                courses.append(item)
    else:
        courses = []
    context = {
        'courses' : courses,
        'authenticated': request.user.is_authenticated,
        'courseForm' : courseForm,
        'instructForm' : instructForm,
    }
    if courseForm.is_valid() and request.user.is_authenticated:
        course = Course(
            title=courseForm.cleaned_data['title'],
            course_number=courseForm.cleaned_data['course_number'],
            instructor=courseForm.cleaned_data['instructor'],
            section=courseForm.cleaned_data['section'],
        )
        course.save()
        course.users.add(request.user)
        #for field in courseForm.cleaned_data['fields']:
        #    course.fields.add(field)
        course.save()
        return redirect('/aggregator') #redirects to clear form

    if instructForm.is_valid():
        instructForm.save()
        messages.success(request, 'Instructor Added!')

    
    return render(request, 'index.html', context=context)

#handles a user logging out, redirects to homepage when finished
def user_logout(request):
    logout(request)
    return redirect('/aggregator/')

#old/outdated function used to handle separate page dedicated to adding Courses, Instructors, and Links
""" def add_course(request):
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
        )
        course.save()
        course.users.add(request.user)
        for field in courseForm.cleaned_data['fields']:
            course.fields.add(field)
        course.save()
        return redirect('/aggregator') #redirects to home page (changed from render to redirect)

    if instructForm.is_valid():
        instructForm.save()

    if fieldForm.is_valid():
        fieldForm.save()

    return render(request, 'course_form.html', context) """

def about(request):
    return render(request, 'about.html')

#loads the details page for an course, creates a form so users can add links to their course 
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

#handles search page and very basic searches for courses using a form
def searchPage(request):
    courses = Course.objects.all()
    form = CourseSearch(request.POST or None)
    if form.is_valid():
        query = form.cleaned_data['Search']
        filtered = []
        if len(query) != None and len(query) != 0:
            for course in courses:
                #checks if the query string is in this mashed string of relevant fields for course models
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

#deletes a course from the database, redirects to a specified redirect url
def removeCourse(request, remCourse, redirectUrl):
    #currently only looks for them based on title so there might be issues with two coursew with same title
    #potentially generate unique id for each course in the future?
    course = Course.objects.get(title=remCourse)
    courseUsers = course.users
    if request.user in courseUsers.all():
        courseUsers.remove(request.user)
        if courseUsers.count() == 0:
            course.delete() 
        messages.success(request, 'Course Removed!')
    if (redirectUrl is '0'):
        return redirect('/aggregator/search')
    else:
        return redirect('/aggregator')

#adds a course to a certain user from the search page
def addCourse(request, addCourse):
    course = Course.objects.get(title=addCourse)
    if not request.user in course.users.all():
        course.users.add(request.user)
        messages.success(request, 'Course Added!')
    return redirect('/aggregator/search')

#removes a field from a certain course
def removeField(request, field, course):
    currentCourse = Course.objects.get(title=course)
    currentField = CourseField.objects.get(name=field)
    if currentField in currentCourse.fields.all():
        currentCourse.fields.remove(currentField)
        messages.success(request, 'Field Removed!')

    return redirect('/aggregator/loadDetails/' + course)
