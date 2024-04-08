from django.contrib import admin
from task1.models import *
# Register your models here.
@admin.register(Student)
class StudentModelAdmin(admin.ModelAdmin):
    list_display = ('id','name','roll','email')
    list_display_links=('name',)