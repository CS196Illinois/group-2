from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('addcourse',views.add_course,name = 'addcourse')
    path('logout/',views.user_logout, name='logout'),
    path('about/', views.about, name='about'),

]