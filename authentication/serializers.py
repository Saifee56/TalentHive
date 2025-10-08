from rest_framework import serializers
from authentication.models import CustomUserModel

class CustomUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'password', 'role', 'professional_bio', 
                  'linked_in', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},
            'company_name': {'required': False} 
        }

    def validate_role(self, value):
        if value not in ['recruiter', 'job_seeker']:
            raise serializers.ValidationError("Invalid role")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUserModel.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user