
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfileInfo(models.Model):
    #Create relationship between user and UserProfileInfo
    #they not inheritance relationship
    #All the attributes from user are passes through a one to one ImageField
    #we can add more if we want

    user = models.OneToOneField(User, on_delete=models.CASCADE,)

#This is what we are adding
#We just add the extra ones that are not built in User stuff
    #portfolio_site = models.URLField(blank=True) #its optional(blanck = True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username
