from rest_framework import serializers
from recruiter.models import (
    RecruiterProfile,
    JobPost,Interview
)

class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=RecruiterProfile
        fields=['id','user','company_name','company_website','position',
                'about_company','company_size','industry',
                'location','created_at','updated_at']
        
    def validate_company_name(self,value):
        if not value or not value.strip():
            raise serializers.ValidationError("Company Name cannot be empty")
        cleaned_name=value.strip()

        if len(cleaned_name) < 2:
            raise serializers.ValidationError("Company name must be at least two characters")
        return cleaned_name
    
class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=JobPost
        fields=['id','recruiter','title','description','requirements',
                'responsibilities','job_type','experience_level',
                'salary_min','salary_max','location','vacancies',
                'application_deadline','created_at','updated_at']
    
    def validate(self,data):

        if data['salary_min'] > data['salary_max']:
            raise serializers.ValidationError("Minimum salary cannot be greater than maximum salary")
        
        return data
    
class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Interview
        fields=['id','application','interview_date','interview_type','meeting_link',
                'location','status','feedback','created_at']
        