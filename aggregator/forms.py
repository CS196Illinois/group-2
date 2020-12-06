from django import forms

from .models import Course, Instructor, CourseField

class CourseSearch(forms.Form):
    Search = forms.CharField(max_length = 100)   
    

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'course_number',
            'instructor',
            'section',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'course_number': forms.TextInput(attrs={'class': 'form-control'}),
            'section': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CourseEditForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'instructor',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'courseTitle edit'}),
            'instructor': forms.Select()
        }
        
class FieldEditForm(forms.ModelForm):
    class Meta:
        model = CourseField
        fields = [
            'name',
            'hyperlink',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'courseField edit'}),
            'hyperlink': forms.TextInput(attrs={'class': 'courseFieldUrl edit'}),
        }

class FieldAddForm(forms.ModelForm):
    private = forms.BooleanField(required=False)
    class Meta:
        model = CourseField
        fields = [
            'name',
            'hyperlink',
            'private',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'courseField edit'}),
            'hyperlink': forms.TextInput(attrs={'class': 'courseFieldUrl edit'}),
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
