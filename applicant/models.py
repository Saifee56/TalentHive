from django.db import models
from authentication.models import CustomUserModel

def upload_resume_path(instance, filename):
    return f"resumes/{instance.user.username}/{filename}"

def upload_cover_letter_path(instance,filename):
    return f"cover/{instance.user.username}"

class ApplicantProfile(models.Model):

    user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name="applicant_profile")
    phone=models.CharField(max_length=25,blank=True,null=True)
    location=models.CharField(max_length=255,blank=True,null=True)
    skills=models.TextField(blank=True,null=True)
    resume=models.FileField(upload_to=upload_resume_path(),null=True,blank=True)
    portfolio_url=models.URLField(blank=True,null=True)
    github_url=models.URLField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    class Meta:
        verbose_name='Applicant Profile'
        verbose_name_plural='Applicant Profiles'
    
    def __str__(self):
        return f"{self.user.username} profile"

class ApplicantEducation(models.Model):
    DEGREE_CHOICES=[
        ('high_school','High School'),
        ('bachelor','Bachelors'),
        ('masters','Masters'),
        ('phd','PhD')

    ]
    applicant=models.ForeignKey(ApplicantProfile,on_delete=models.CASCADE,related_name='education')
    institution=models.CharField(max_length=255)
    degree=models.CharField(max_length=40,choices=DEGREE_CHOICES)
    fields_of_study=models.CharField(max_length=255)
    start_date=models.DateField()
    end_date=models.DateField(blank=True,null=True)

    class Meta:
        verbose_name='Applicant Education'
        verbose_name_plural='Applicant Educations'

    def __str__(self):
        return f"{self.applicant.user.username}--->{self.degree}---> {self.institution}"

class ApplicantWorkExperience(models.Model):
    applicant=models.ForeignKey(ApplicantProfile,on_delete=models.CASCADE,related_name='work_experience')
    company=models.CharField(max_length=255)
    designation=models.CharField(max_length=255)
    start_date=models.DateField()
    end_date=models.DateField(blank=True,null=True)

    class Meta:
        verbose_name='Applicant Work Experience'
        verbose_name_plural='Applicant Work Experiences'



