from rest_framework import serializers
from authentication.models import CustomUserModel

class CustomUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'password', 'role', 'professional_bio', 'company_name', 
                  'linked_in', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},
            'company_name': {'required': False} 
        }

    def validate_role(self, value):
        if value not in ['recruiter', 'job_seeker']:
            raise serializers.ValidationError("Invalid role")
        return value

    def validate(self, attrs):
        # Company name required for recruiters
        if attrs.get('role') == 'recruiter' and not attrs.get('company_name'):
            raise serializers.ValidationError({
                'company_name': 'Company name is required for recruiters'
            })
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUserModel.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user