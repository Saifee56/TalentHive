from django.contrib import admin
from .models import (
    ApplicantProfile,
    ApplicantEducation,
    ApplicantWorkExperience,
    JobApplication,
    SavedJob
)

@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'location', 'portfolio_url', 'created_at')
    search_fields = ('user__username', 'phone', 'location', 'skills')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(ApplicantEducation)
class ApplicantEducationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'degree', 'institution', 'start_date', 'end_date')
    search_fields = ('applicant__user__username', 'institution', 'degree')
    list_filter = ('degree', 'start_date', 'end_date')
    ordering = ('-start_date',)


@admin.register(ApplicantWorkExperience)
class ApplicantWorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'company', 'designation', 'start_date', 'end_date')
    search_fields = ('applicant__user__username', 'company', 'designation')
    list_filter = ('start_date', 'end_date')
    ordering = ('-start_date',)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'status', 'applied_at', 'reviewed_at')
    search_fields = ('applicant__username', 'job__title', 'status')
    list_filter = ('status', 'applied_at', 'reviewed_at')
    ordering = ('-applied_at',)


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
    search_fields = ('user__username', 'job__title')
    list_filter = ('saved_at',)
    ordering = ('-saved_at',)
