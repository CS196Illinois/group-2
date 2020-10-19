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

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = [
            'last_name',
            'first_name',
            'department',
        ]
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FieldForm(forms.ModelForm):
    class Meta:
        model = CourseField
        fields = [
            'name',
            'hyperlink',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'hyperlink': forms.URLInput(attrs={'class': 'form-control'}),
        }
