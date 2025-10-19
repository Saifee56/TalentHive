from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from recruiter.models import RecruiterProfile
from recruiter.serializers import RecruiterProfileSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction

class RecruiterProfileViewset(viewsets.ModelViewSet):

    permission_classes=[IsAuthenticated]
    serializer_class=RecruiterProfileSerializer
    queryset=RecruiterProfile.objects.all()

    def get_queryset(self):
        """
        Users can only see their own profile
        """
        return RecruiterProfile.objects.filter(user=self.request.user)

    @action(detail=False,methods=['post'],url_path='create-recruiter-profile')
    def create_recruiter_profile(self,request):

        if RecruiterProfile.objects.filter(user=request.user).exists():
            return Response({
                "success":False,
                "message":"You already have a recruiter profile"
        })

        try:
            with transaction.atomic():               
                    data=request.data
                    serializer=RecruiterProfileSerializer(data=data)
                    if not serializer.is_valid():
                        return Response(
                            {
                                "success":False,
                                "message":"Recruiter Profile creation failed",
                                "data":serializer.errors
                            },status=status.HTTP_400_BAD_REQUEST
                        )
                    serializer.save(user=request.user)
                    return Response({
                         "success":True,
                         "message":f"Recruiter profile created successfully",
                         "data":serializer.data
                    },status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                 "success":False,
                 "errors":f"An error occurred {str(e)}"
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True,methods=['patch'],url_path='update-recruiter-profile')
    def update_recruiter_profile(self,request,pk=None):
        recruiter=get_object_or_404(RecruiterProfile,pk=pk)

        if recruiter.user != request.user:
            return Response({
                "success":False,
                "message":"You are not allowed to make any changes"
            },status=status.HTTP_403_FORBIDDEN)

        try:
            with transaction.atomic(): 
                   if not recruiter:
                        return Response({
                             "message":"Recruiter ID is required for update"
                        })
                   serializer=RecruiterProfileSerializer(recruiter,data=request.data,partial=True)
                   if not serializer.is_valid():
                        return Response(
                            {
                                "success":False,
                                "message":"Recruiter Profile update failed",
                                "data":serializer.errors
                            },status=status.HTTP_400_BAD_REQUEST
                        )
                   serializer.save(user=request.user)
                   return Response({
                         "success":True,
                         "message":"Recruiter profile updated successfully",
                         "data":serializer.data
                    },status=status.HTTP_201_CREATED)
        except Exception as e:
             return Response({
                  "success":False,
                  "message":f"An error occured {str(e)}"
             })

    @action(detail=True, methods=['delete'], url_path='delete-recruiter-profile')
    def delete_recruiter_profile(self, request, pk=None):
        recruiter = get_object_or_404(RecruiterProfile, pk=pk)

        if recruiter.user != request.user:
            return Response({
                 "success":False,
                 "message":"You are not allowed to delete"
            },status=status.HTTP_403_FORBIDDEN)
        
        try:
            with transaction.atomic():
                recruiter.delete()
                return Response({
                    "success": True,
                    "message": "Recruiter profile deleted successfully"
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        