from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from authors.apps.authentication.models import User
from django.contrib.postgres.fields import ArrayField


class UserProfile(models.Model):
    photo =  models.URLField(blank=True)
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    bio = models.TextField(blank=True)
    fun_fact = models.TextField(blank=True)
  
    time_when_updated = models.DateTimeField(auto_now=True)
    favorite_article = ArrayField(models.CharField(max_length=100), default=list)
 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile=UserProfile(user=instance)
        return user_profile.save()
        