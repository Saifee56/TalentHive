from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from applicant.models import ApplicantProfile
from applicant.serializers import ApplicantProfileSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction

class ApplicantProfileViewset(viewsets.ModelViewSet):

    permission_classes=[AllowAny]
    serializer_class=ApplicantProfileSerializer

    @action(detail=False,methods=['post'],url_path='create-applicant-profile')
    def create_applicant_profile(self,request):
        try:
            with transaction.atomic():
                data=request.data
                serializer=ApplicantProfileSerializer(data=data)
                if not serializer.is_valid():
                    return Response({
                        "success":False,
                        "message":"Applicant profile creation failed",
                        "data":serializer.errors
                    },status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response({
                    "success":True,
                    "message":"Applicant profile created successfully",
                    "data":serializer.data
                },status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "success":False,
                "errors":f"An error occurred {str(e)}"
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True,methods=['PATCH'],url_path='update-applicant-profile')
    def update_applicant_profile(self,request,pk=None):
        applicant_profile=get_object_or_404(ApplicantProfile,pk=pk)

        try:
            with transaction.atomic():
                if not applicant_profile:
                    return Response({
                        "message":"Applicant ID is required for update"
                    })
                data=request.data
                serializer=ApplicantProfileSerializer(applicant_profile,data=data)
                if not serializer.is_valid():
                    return Response({
                        "success":False,
                        "message":"Applicant profile update failed",
                        "data":serializer.errors
                    },status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response({
                    "message":True,
                    "message":"Applicant Profile updated successfully",
                    "data":serializer.data
                },status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "success":False,
                "message":f"An error occurred {str(e)}"
            })
    @action(detail=True, methods=['delete'], url_path='delete-recruiter-profile')
    def delete_recruiter_profile(self, request, pk=None):
        applicant_profile = get_object_or_404(ApplicantProfile, pk=pk)
        
        try:
            with transaction.atomic():
                applicant_profile.delete()
                return Response({
                    "success": True,
                    "message": "Recruiter profile deleted successfully"
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        
