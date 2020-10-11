from django.shortcuts import render
from aggregator.models import CourseField, Course, Instructor

# Create your views here.
def index(request):
    courses = Course.objects.all()
    context = {
        'courses' : courses,
    }
    return render(request, 'index.html', context=context)