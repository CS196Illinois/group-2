from django import forms

from .models import Course, Instructor, CourseField

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'course_number',
            'instructor',
            'section',
            'fields'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'course_number': forms.TextInput(attrs={'class': 'form-control'}),
            'section': forms.TextInput(attrs={'class': 'form-control'}),
        }