from rest_framework import serializers
from applicant.models import ApplicantProfile,ApplicantEducation,ApplicantWorkExperience,JobApplication,SavedJob
from django.utils import timezone

class ApplicantProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=ApplicantProfile
        fields=['id','user','phone','location','skills','resume','portfolio_url',
                'github_url','created_at','updated_at']
        


class ApplicantEducationSerializer(serializers.ModelSerializer):

    class Meta:
        model=ApplicantEducation
        fields=['id','applicant','institution','degree','fields_of_study','start_date','end_date']

    def validate(self,data):

        start_date=data.get('start_date')
        end_date=data.get('end_date')

        if start_date > end_date:
            raise serializers.ValidationError("End date must be after start date")
        
        if start_date and start_date > timezone.now().date():
            raise serializers.ValidationError("Start date cannot be in the future")
        return data

class ApplicantWorkExperience(serializers.ModelSerializer):

    class Meta:
        model=ApplicantWorkExperience
        fields=['id','applicant','company','start_date','end_date']

    def get_is_current(self,obj):
        """checks if this is the current job"""
        return obj.end_date is None
    
    def get_duration(self,obj):
        """calculate job duration"""

        if obj.end_date:
            delta=obj.end_date-obj.start_date
        else:
            delta=timezone.now().date()-obj.start_date
        return round(delta.days/30)
    
    def validate(self, attrs):
        """Cross-field validation"""
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        
        if start_date and start_date > timezone.now().date():
            raise serializers.ValidationError({
                'start_date': 'Start date cannot be in the future'
            })
        
        if end_date:
            if end_date < start_date:
                raise serializers.ValidationError({
                    'end_date': 'End date must be after start date'
                })
            
            if end_date > timezone.now().date():
                raise serializers.ValidationError({
                    'end_date': 'End date cannot be in the future'
                })
        
        return attrs
    
    class JobApplicationSerializer(serializers.ModelSerializer):
        class Meta:
            model=JobApplication
            fields='__all__'

    class SavedJobSerializer(serializers.ModelSerializer):
        class Meta:
            model=SavedJob
            fields='__all__'
