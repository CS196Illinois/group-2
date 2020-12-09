from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    #path('addcourse',views.add_course,name = 'addcourse'),
    path('logout/',views.user_logout, name='logout'),
    path('about/', views.about, name='about'),
    path('loadDetails/<course_load>/', views.loadDetails, name = "loadDetails"),
    path('search', views.searchPage, name = "search"),
    path('remove/<str:pk>/<redirectUrl>/', views.removeCourse, name= "removeCourse"),
    path('add/<str:pk>/', views.addCourse, name= "addCourse"),
    path('removeField/<str:fieldPk>/<str:pk>/', views.removeField, name= "removeField"),
    path('editCourse/<str:coursePk>/', views.editCourse, name="editCourse"),
    path('addField/<str:coursePk>/', views.addField, name="addField"),
    path('addInstructor/', views.addInstructor, name="addInstructor"),
    path('createCourse/', views.createCourse, name="createCourse"),
]
