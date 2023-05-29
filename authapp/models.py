from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField



class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    resume = models.FileField(upload_to="userResumes/", max_length=540, blank=True, null=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
   
    
    #Socials
    website = models.CharField(max_length=250, null=True, blank=True)
    github = models.CharField(max_length=250, null=True, blank=True)
    linkedin = models.CharField(max_length=250, null=True, blank=True)
    twitter = models.CharField(max_length=250, null=True, blank=True)
    instagram = models.CharField(max_length=250, null=True, blank=True)
    facebook = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class UserSocials(models.Model):
    profile = models.OneToOneField(Profile , on_delete=models.CASCADE)
    #Socials
    website = models.CharField(max_length=250, null=True, blank=True)
    github = models.CharField(max_length=250, null=True, blank=True)
    linkedin = models.CharField(max_length=250, null=True, blank=True)
    twitter = models.CharField(max_length=250, null=True, blank=True)
    instagram = models.CharField(max_length=250, null=True, blank=True)
    facebook = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.profile.user.username