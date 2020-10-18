from django.shortcuts import render
from aggregator.models import CourseField, Course, Instructor
from django.contrib.auth import logout

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

def about(request):
    return render(request, 'about.html')