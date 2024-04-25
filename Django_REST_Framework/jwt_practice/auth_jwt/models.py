from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserRole(models.Model):
    role_list=models.CharField(max_length=70)
    def __str__(self):
        return self.role_list

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.ForeignKey(UserRole,on_delete=models.PROTECT,null=True)
    role_name = models.CharField(max_length=70)
    def __str__(self):
        return self.role_name