from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class FriendList(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user1',default="0")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user2',default="0")
    confirmed = models.IntegerField(default=0)

    def __str__(self):
        return self.user1.username + " " + self.user2.username 
