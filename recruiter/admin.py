from django.contrib import admin
from .models import RecruiterProfile, JobPost, Interview


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'company_name', 'position', 'industry', 'location', 'created_at')
    search_fields = ('user__username', 'company_name', 'industry', 'location')
    list_filter = ('industry', 'company_size', 'created_at')
    ordering = ('-created_at',)


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = (
        'id','title', 'recruiter', 'job_type', 'experience_level',
        'salary_min', 'salary_max', 'location', 'vacancies', 'application_deadline', 'created_at'
    )
    search_fields = ('title', 'recruiter__company_name', 'location', 'experience_level', 'job_type')
    list_filter = ('job_type', 'experience_level', 'application_deadline', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'application_deadline'


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = (
        'application', 'interview_date', 'interview_type',
        'status', 'location', 'meeting_link', 'created_at'
    )
    search_fields = (
        'application__applicant__username',
        'application__job__title',
        'interview_type',
        'status'
    )
    list_filter = ('status', 'interview_date', 'created_at')
    ordering = ('-interview_date',)
