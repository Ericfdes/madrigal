from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

JOB_TYPE = (("1", "Full time"), ("2", "Part time"), ("3", "Internship"))

JOB_STATUS = (
    ("1", "Applied"),
    ("2", "Received"),
    ("3", "Review Pending"),
    ("4", "Review Complete"),
    ("5", "Accepted"),
    ("6", "Rejected"),
    )

APPLY_METHOD = (
    ("1", "CV"),
    ("2", "LinkedIn"),
    )

class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

#Does not work on Windows
# def create_path(instance, filename):
#     return os.path.join(
#         'resume',
#         str(instance.job).replace(' ', '_'),
#         instance.first_name + "_"+ instance.last_name,
#         str(filename).replace(' ', '_')
#     )


class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    qualification = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    last_date = models.DateField(default=datetime.today, blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    vacancy = models.IntegerField(default=1)
    tags = models.ManyToManyField(Tag)

    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_description = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("jobs:jobs-detail", args=[self.job_id])

    def __str__(self):
        return f"{str(self.job_id)} {str(self.title)}"



class Services(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo_icon = models.CharField(max_length=100)
    logo_color = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name
    
class JobApplication(models.Model):
    application_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    provider = models.CharField(choices=APPLY_METHOD, max_length=50, default=1)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, default='')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    applied_on = models.DateField(default=datetime.today)
    resume = models.FileField(upload_to="resume/", max_length=540, blank=True, null=True)
    status = models.CharField(choices=JOB_STATUS, max_length=50, default=1)
    response = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        ordering = ["-applied_on"]

    def __str__(self):
        return f"{str(self.job)} Job Application| Date: {str(datetime.date(datetime.now()))}"
    




