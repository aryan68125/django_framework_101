from django.contrib import admin
from api.models import Singer, Song
# Register your models here.
@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    list_display=('id','name','gender')
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display=('id','singer','title','duration')