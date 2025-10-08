from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from recruiter.models import RecruiterProfile
from recruiter.serializers import RecruiterProfileSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction

class RecruiterProfileViewset(viewsets.ModelViewSet):

    permission_classes=[AllowAny]
    serializer_class=RecruiterProfileSerializer

    @action(detail=False,methods=['post'],url_path='create-recruiter-profile')
    def create_recruiter_profile(self,request):
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
                    serializer.save()
                    return Response({
                         "success":True,
                         "message":"Recruiter profile created successfully",
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
                   serializer.save()
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

              
                        