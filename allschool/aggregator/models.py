from django.db import models

# Course Fields 
# Example:
#     name : Discussion
#     hyperlink : zoom.com/here 
class CourseFields(models.Model):
    name = models.CharField(max_length=20)
    hyperlink = models.URLField()

    def __str__(self):
        return self.name


class Course(models.Model):
    # Course Descriptors
    title = models.CharField(max_length=25)
    course_number = models.IntegerField(max_length=10, blank=True)
    instructor = models.CharField(max_length=30, blank=True)
    section = models.IntegerField(max_length=5, blank=True)
    created_on = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    fields = models.ForeignKey(  # This is where we'll have the fields like discussion links, lab links, etc.
        CourseFields,
        on_delete=models.CASCADE, # ensure that if the course is deleted, the fields will also be deleted.
    )
    
    def __str__(self):
        return self.title


    