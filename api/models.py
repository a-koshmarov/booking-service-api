from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class User(AbstractUser):
    pass

@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def my_callback(sender, instance, *args, **kwargs):
    instance.is_active = True

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

class Room(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Booking(models.Model):
    workplace = models.ForeignKey(Room, on_delete=models.CASCADE)
    booked = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.user:
            return "{} | {} - {} | {}".format(
                self.workplace, 
                self.start_time.strftime("%b %d %Y %H:%M"), 
                self.end_time.strftime("%b %d %Y %H:%M"), 
                self.user)
        else: 
            return "{} | {} - {} | not booked".format(
                self.workplace, 
                self.start_time.strftime("%b %d %Y %H:%M"), 
                self.end_time.strftime("%b %d %Y %H:%M"))

