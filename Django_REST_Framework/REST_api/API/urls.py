from django.urls import path
from API.views import *
urlpatterns = [
    path('student_detail/<int:Student_ID>',student_detail,name="student_detail"),
    path('',student_list,name="student_list"),
    path('create_student',create_student,name="create_student"),
    path('update_student',update_student,name="update_student"),
]