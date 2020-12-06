from django.shortcuts import render, redirect
from aggregator.models import CourseField, Course, Instructor
from django.contrib.auth import logout
from django.contrib import messages
from .forms import CourseForm, InstructorForm, FieldForm, CourseSearch, CourseEditForm, FieldEditForm, FieldAddForm
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# Create your views here.
def index(request):
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
        'editing': '', #title of the course that is being edited
        'addingField': '',
        'currentUser': request.user,
    }

    return render(request, 'index.html', context=context)

def addInstructor(request):
    instructForm = InstructorForm(request.POST or None)

    if instructForm.is_valid():
        instructForm.save()
        messages.success(request, 'Instructor Added!')
    return redirect('/aggregator/')

def createCourse(request):
    if request.user.is_authenticated:
        course = Course(title='My Course', course_number=0, instructor=None, section='a')
        course.save()
        course.users.add(request.user)
        course.save()
    return redirect('/aggregator/')

#handles a user logging out, redirects to homepage when finished
def user_logout(request):
    logout(request)
    return redirect('/aggregator/')

def about(request):
    return render(request, 'about.html')

#old/outdated function that loads the details page for an course, creates a form so users can add links to their course 
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
    if redirectUrl == '0':
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

    return redirect('/aggregator')

def editCourse(request, title):
    form = CourseEditForm(request.POST or None)
    course = Course.objects.get(title=title)
    formFields = { }
    for field in course.fields.all():
        formFields[field.name] = FieldEditForm(request.POST or None, prefix = field.name)

    if form.is_valid() and request.user.is_authenticated:
        course.title = form.cleaned_data['title']
        course.instructor = form.cleaned_data['instructor']
        course.save()
        for key in formFields:
            currentForm = formFields[key]
            if (currentForm.is_valid()):
                currentField = course.fields.all().get(name=key)
                currentField.name = currentForm['name'].value()
                currentField.hyperlink = currentForm['hyperlink'].value()
                currentField.save()
        return redirect('/aggregator/')
    else:
        if request.user.is_authenticated:
            courses = []
            allCourses = Course.objects.all()
            for item in allCourses:
                if request.user in item.users.all():
                    courses.append(item)
        else:
            courses = []

        form.fields['title'].initial = title
        for key in formFields:
            currentForm = formFields[key]
            currentField = course.fields.all().get(name=key)
            currentForm.fields['name'].initial = currentField.name
            currentForm.fields['hyperlink'].initial = currentField.hyperlink
        
        instructForm = InstructorForm(request.POST or None)
        context = {
            'courses' : courses,
            'authenticated': request.user.is_authenticated,
            'editing': title,
            'form': form,
            'formField' : formFields,
            'addingField': '',
            'instructForm': instructForm,
        }
        return render(request, 'index.html', context)

def addField(request, title):
    course = Course.objects.get(title=title)
    formField = FieldAddForm(request.POST or None)
    formField.fields['name'].initial = 'Insert Name'
    formField.fields['hyperlink'].initial = "Link URL"
    formField.fields['private'].initial = False

    if formField.is_valid() and request.user.is_authenticated:
        isPrivate = formField.cleaned_data['private']
        if isPrivate == None:
            isPrivate = False
        newField = CourseField(
            name = formField.cleaned_data['name'],
            hyperlink = formField.cleaned_data['hyperlink'],
            private = isPrivate,
            user = request.user,
        )
        newField.save()
        course.fields.add(newField)
        course.save()
        return redirect('/aggregator/')
    else:
        if request.user.is_authenticated:
            courses = []
            allCourses = Course.objects.all()
            for item in allCourses:
                if request.user in item.users.all():
                    courses.append(item)
        else:
            courses = []
        
        context = {
            'courses' : courses,
            'authenticated': request.user.is_authenticated,
            'editing': '',
            'formField' : formField,
            'addingField': title,
        }
        return render(request, 'index.html', context)