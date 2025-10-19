from django.db import models
# from authentication.models import CustomUserModel
# from applicant.models import JobApplication
from django.db.models.signals import post_delete
from django.dispatch import receiver    

class RecruiterProfile(models.Model):
    user=models.OneToOneField('authentication.CustomUserModel',on_delete=models.CASCADE,related_name='recruiter_profile')
    company_name=models.CharField(max_length=255)
    company_website=models.URLField(blank=True,null=True)
    position=models.CharField(max_length=20,null=True,blank=True)
    about_company=models.TextField()
    company_size=models.CharField(max_length=50,blank=True,null=True)
    industry=models.CharField(max_length=50,null=True,blank=True)
    location=models.CharField(max_length=255,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}-{self.company_name}"
    




class JobPost(models.Model):
    JOB_TYPE_CHOICES=[
        ('full_time','Full Time'),
        ('part_time','Part Time'),
        ('contract','Contract'),
        ('internship','Internship'),
        ('remote','Remote')
    ]

    EXPERIENCE_CHOICES=[
        ('entry','0-1 years'),
        ('junior','1-3 years'),
        ('mid','3-5 years'),
        ('senior','5+ years')
    ]

    recruiter=models.ForeignKey(RecruiterProfile,on_delete=models.CASCADE,related_name='job_posts')
    title=models.CharField(max_length=255)
    description=models.TextField()
    requirements=models.TextField()
    responsibilities=models.TextField()
    job_type=models.CharField(max_length=20,choices=JOB_TYPE_CHOICES)
    experience_level=models.CharField(max_length=80,choices=EXPERIENCE_CHOICES)
    salary_min=models.DecimalField(max_digits=10,decimal_places=2)
    salary_max=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    location=models.CharField(max_length=255)
    vacancies=models.IntegerField(default=1)
    application_deadline=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    class Meta:
        verbose_name='Job Post'
        verbose_name_plural='Job Posts'
    
    def __str__(self):
        return f"{self.title} posted by {self.recruiter.company_name}"

class Interview(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    application = models.ForeignKey('applicant.JobApplication', on_delete=models.CASCADE, related_name='interviews')
    interview_date = models.DateTimeField()
    interview_type = models.CharField(max_length=50)
    meeting_link = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview - {self.application.job.title}"
    
@receiver(post_delete, sender=RecruiterProfile)
def delete_user_when_recruiter_deleted(sender, instance, **kwargs):
    """
    Delete the linked user when a recruiter profile is deleted.
    """
    if instance.user:
        instance.user.delete()