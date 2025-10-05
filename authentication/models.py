from django.db import models
from django.contrib.auth.models import AbstractUser


def upload_profile_picture(instance, filename):
    role = instance.role if hasattr(instance, 'role') else 'user'
    username = instance.username if hasattr(instance, 'username') else 'unknown'
    return f"profile_pictures/{role}_{username}/{filename}"

class CustomUserModel(AbstractUser):

    ROLE_CHOICES=(
        ('recruiter','RECRUITER'),
        ('job_seeker','Job Seeker')
    )
    professional_bio=models.TextField()
    company_name=models.CharField(max_length=255,null=True,blank=True)
    linked_in=models.URLField(max_length=255,blank=True,null=True)
    profile_picture=models.ImageField(upload_to=upload_profile_picture,null=True,blank=True)
    role=models.CharField(max_length=25,choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username}--{self.role}"

