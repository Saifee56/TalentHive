from django.db import models
from authentication.models import CustomUserModel

class RecruiterProfile(models.Model):
    user=models.OneToOneField(CustomUserModel,on_delete=models.CASCADE,related_name='recruiter_profile')
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
    responsibilities=models.TextField(blank=True,null=True)
    job_type=models.CharField(max_length=20,choices=JOB_TYPE_CHOICES)
    experience_level=models.CharField(max_length=80,choices=EXPERIENCE_CHOICES)
    salary_min=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    salary_max=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    location=models.CharField(max_length=255)
    vacancies=models.IntegerField(default=1)
    application_deadline=models.DateField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    class Meta:
        verbose_name='Job Post'
        verbose_name_plural='Job Posts'
    
    def __str__(self):
        return f"{self.title} posted by {self.recruiter.company_name}"

# class Interview(models.Model):

#     STATUS_CHOICES=[
#         ('completed','COMPLETED'),
#         ('scheduled','Scheduled'),
#         ('cancelled','Cancelled')
#     ]
